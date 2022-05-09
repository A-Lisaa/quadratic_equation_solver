RawTermsSide = list[str]
RawTerms = tuple[RawTermsSide, RawTermsSide]

RawCoefficient = str
RawCoefficientSide = list[RawCoefficient]
RawCoefficient = tuple[RawCoefficientSide, RawCoefficientSide]
RawCoefficients = tuple[RawCoefficient, RawCoefficient, RawCoefficient]

Coefficient = tuple[str, str]
OneSideCoefficients = list[Coefficient]
BothSidesCoefficients = tuple[OneSideCoefficients, OneSideCoefficients]
AllCoefficients = tuple[BothSidesCoefficients, BothSidesCoefficients, BothSidesCoefficients]

Roots = tuple[float, float] | tuple[float, None] | tuple[None, None]
