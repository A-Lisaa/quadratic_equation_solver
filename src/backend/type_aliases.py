Coefficient = tuple[str, str]
OneSideCoefficients = list[Coefficient]
BothSidesCoefficients = tuple[OneSideCoefficients, OneSideCoefficients]
AllCoefficients = tuple[BothSidesCoefficients, BothSidesCoefficients, BothSidesCoefficients]

Roots = tuple[float, float] | tuple[float, None] | tuple[None, None]
