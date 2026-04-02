import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 400
    learning_rate: float = 0.005
    num_steps: int = 20000
    warmup_steps: int = 2000


class C3Optimizer:
    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 0.5
        self.dx = self.domain_width / self.hypers.num_intervals

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        integral_f = jnp.sum(f_values) * self.dx
        eps = 1e-9
        integral_f_sq_safe = jnp.maximum(integral_f ** 2, eps)
        N = self.hypers.num_intervals
        padded_f = jnp.pad(f_values, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        conv_f_f = jnp.fft.ifft(fft_f * fft_f).real
        scaled_conv_f_f = conv_f_f * self.dx
        max_abs_conv = jnp.max(jnp.abs(scaled_conv_f_f))
        c3_ratio = max_abs_conv / integral_f_sq_safe
        return c3_ratio

    def train_step(self, f_values, opt_state):
        loss, grads = jax.value_and_grad(self._objective_fn)(f_values)
        updates, opt_state = self.optimizer.update(grads, opt_state, f_values)
        f_values = optax.apply_updates(f_values, updates)
        return f_values, opt_state, loss

    def run_optimization(self):
        schedule = optax.warmup_cosine_decay_schedule(
            init_value=0.0,
            peak_value=self.hypers.learning_rate,
            warmup_steps=self.hypers.warmup_steps,
            decay_steps=self.hypers.num_steps - self.hypers.warmup_steps,
            end_value=self.hypers.learning_rate * 1e-4,
        )
        self.optimizer = optax.adam(learning_rate=schedule)
        key = jax.random.PRNGKey(42)
        f_values = jax.random.normal(key, (self.hypers.num_intervals,))
        opt_state = self.optimizer.init(f_values)
        train_step_jit = jax.jit(self.train_step)
        for step in range(self.hypers.num_steps):
            f_values, opt_state, loss = train_step_jit(f_values, opt_state)
        return f_values


def solve():
    hypers = Hyperparameters()
    optimizer = C3Optimizer(hypers)
    optimized_f = optimizer.run_optimization()
    return list(np.array(optimized_f))
