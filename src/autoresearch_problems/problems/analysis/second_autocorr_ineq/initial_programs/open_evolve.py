import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 50
    learning_rate: float = 0.01
    num_steps: int = 15000
    warmup_steps: int = 1000


class C2Optimizer:
    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        f_non_negative = jax.nn.relu(f_values)
        N = self.hypers.num_intervals
        padded_f = jnp.pad(f_non_negative, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real
        num_conv_points = len(convolution)
        h = 1.0 / (num_conv_points + 1)
        y_points = jnp.concatenate([jnp.array([0.0]), convolution, jnp.array([0.0])])
        y1, y2 = y_points[:-1], y_points[1:]
        l2_norm_squared = jnp.sum((h / 3) * (y1 ** 2 + y1 * y2 + y2 ** 2))
        norm_1 = jnp.sum(jnp.abs(convolution)) / (len(convolution) + 1)
        norm_inf = jnp.max(jnp.abs(convolution))
        denominator = norm_1 * norm_inf
        c2_ratio = l2_norm_squared / denominator
        return -c2_ratio

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
        f_values = jax.random.uniform(key, (self.hypers.num_intervals,))
        opt_state = self.optimizer.init(f_values)
        train_step_jit = jax.jit(self.train_step)
        for step in range(self.hypers.num_steps):
            f_values, opt_state, loss = train_step_jit(f_values, opt_state)
        return jax.nn.relu(f_values)


def solve():
    hypers = Hyperparameters()
    optimizer = C2Optimizer(hypers)
    optimized_f = optimizer.run_optimization()
    return list(np.array(optimized_f))
