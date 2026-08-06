from __future__ import annotations

import random
from collections import Counter, defaultdict
from collections.abc import Hashable, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Generic, TypeVar

Token = TypeVar("Token", bound=Hashable)
Context = tuple[Token, ...]


@dataclass
class NGramModel(Generic[Token]):
    """Maximum-likelihood n-context model with deterministic backoff.

    `n` is the number of previous tokens used as context.

    - n=0: unconditional token-frequency model
    - n=1: one previous token
    - n=2: two previous tokens
    """
    n: int
    counts: dict[Context[Token], Counter[Token]] = field(
        default_factory=lambda: defaultdict(Counter)
    )
    vocabulary: Counter[Token] = field(default_factory=Counter)

    def __post_init__(self) -> None:
        if self.n < 0:
            raise ValueError("n must be nonnegative")

    def fit(self, tokens: Sequence[Token]) -> "NGramModel[Token]":
        self.counts.clear()
        self.vocabulary.clear()
        self.vocabulary.update(tokens)

        for index, token in enumerate(tokens):
            start = max(0, index - self.n)
            context = tuple(tokens[start:index])
            if len(context) == self.n:
                self.counts[context][token] += 1

        return self

    def distribution(
        self,
        context: Iterable[Token] = (),
    ) -> Counter[Token]:
        requested = tuple(context)

        if self.n == 0:
            return self.vocabulary.copy()

        for width in range(min(self.n, len(requested)), -1, -1):
            suffix = requested[-width:] if width else ()
            if width == self.n and suffix in self.counts:
                return self.counts[suffix].copy()

        return self.vocabulary.copy()

    def sample_next(
        self,
        context: Iterable[Token] = (),
        *,
        rng: random.Random | None = None,
    ) -> Token:
        generator = rng or random
        distribution = self.distribution(context)

        if not distribution:
            raise RuntimeError("model has no fitted tokens")

        choices = list(distribution)
        weights = [distribution[token] for token in choices]
        return generator.choices(choices, weights=weights, k=1)[0]

    def generate(
        self,
        length: int,
        *,
        seed: Sequence[Token] = (),
        random_seed: int | None = None,
    ) -> list[Token]:
        if length < 0:
            raise ValueError("length must be nonnegative")

        rng = random.Random(random_seed)
        generated = list(seed)

        while len(generated) < length:
            generated.append(
                self.sample_next(generated, rng=rng)
            )

        return generated[:length]

    def training_context_count(self) -> int:
        return len(self.counts)
