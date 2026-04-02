import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 600
    learning_rate: float = 0.005
    end_lr_factor: float = 1e-4
    num_steps: int = 40000
    warmup_steps: int = 2000


class AutocorrelationOptimizer:
    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 0.5
        self.dx = self.domain_width / self.hypers.num_intervals

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        f_non_negative = jax.nn.relu(f_values)
        integral_f = jnp.sum(f_non_negative) * self.dx
        eps = 1e-9
        integral_f_safe = jnp.maximum(integral_f, eps)
        N = self.hypers.num_intervals
        padded_f = jnp.pad(f_non_negative, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        fft_conv = fft_f * fft_f
        conv_f_f = jnp.fft.ifft(fft_conv).real
        scaled_conv_f_f = conv_f_f * self.dx
        max_conv = jnp.max(scaled_conv_f_f)
        c1_ratio = max_conv / (integral_f_safe ** 2)
        return c1_ratio

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
            end_value=self.hypers.learning_rate * self.hypers.end_lr_factor,
        )
        self.optimizer = optax.adam(learning_rate=schedule)
        key = jax.random.PRNGKey(42)
        N = self.hypers.num_intervals
        f_values = jnp.zeros((N,))
        start_idx, end_idx = N // 4, 3 * N // 4
        f_values = f_values.at[start_idx:end_idx].set(1.0)
        f_values += 0.05 * jax.random.uniform(key, (N,))
        opt_state = self.optimizer.init(f_values)
        train_step_jit = jax.jit(self.train_step)
        for step in range(self.hypers.num_steps):
            f_values, opt_state, loss = train_step_jit(f_values, opt_state)
        return jax.nn.relu(f_values), loss


def solve():
    hypers = Hyperparameters()
    optimizer = AutocorrelationOptimizer(hypers)
    optimized_f, _ = optimizer.run_optimization()
    return list(np.array(optimized_f))
