def get_refined_matcher():
    rules = {
        # 1. Mathematics (6-9)
        "1.A": lambda c, t, o, it: (
            c in ["MATH 112", "MATH 113", "MATH 302", "PHSCS 121"] and (
                any(w in t for w in ["analytic geometry", "trigonometr", "logarithm", "polar coordinate", "parametric equation", "geometric interpretation"])
                or (c == "MATH 113" and "parametric" in t)
            )
        ),
        "1.B": lambda c, t, o, it: (
            c in ["MATH 112", "MATH 113", "MATH 302", "CBE 263", "PHSCS 121"] and (
                any(w in t for w in ["calculus", "derivative", "differentiat", "integral", "integrat", "fundamental theorem of calculus", "multivariable calculus", "limits", "extrema"])
            )
        ),
        "1.C": lambda c, t, o, it: (
            any(w in t for w in ["differential equation", "ordinary differential", "partial differential", "ode", "pde", "laplace", "boundary value", "initial value"])
            and c in ["MATH 303", "CBE 436", "CBE 374", "CBE 376", "CBE 386"]
        ),
        "1.D": lambda c, t, o, it: (
            any(w in t for w in ["numerical method", "numerical analysis", "curve fit", "newton-raphson", "fourier series", "error propagation", "numerical integration", "euler", "runge-kutta", "finite difference", "quadrature"])
            or (c == "CBE 263" and ("spreadsheets" in t or "structured programming" in t or "complex numerical" in t or "curve fitting" in t or "equation-solving" in t))
            or (c == "MATH 302" and "numerical methods" in t)
            or (c == "MATH 303" and "fourier" in t)
        ),
        "1.E": lambda c, t, o, it: (
            any(w in t for w in ["matrix algebra", "linear algebra", "systems of equations", "eigenvalue", "eigenvector", "determinant", "gaussian elimination", "matrix operations"])
            or (c == "MATH 302" and "linear algebra" in t)
            or (c == "CBE 263" and ("solving equations" in t or "equation-solving" in t))
        ),
        "1.F": lambda c, t, o, it: (
            any(w in t for w in ["significant figure", "unit conversion", "dimensional consistency", "order of magnitude estimate", "accuracy, precision", "error analysis"])
            or (c in ["CBE 263", "CBE 170", "CBE 273", "STAT 121", "PHSCS 121", "CHEM 111"] and any(w in t for w in ["unit conversion", "dimensional consistency", "order of magnitude estimate", "assess reasonableness of solution"]))
        ),

        # 2. Probability and Statistics (4-6)
        "2.A": lambda c, t, o, it: (
            c in ["STAT 121", "CBE 311", "CBE 451"] and (
                any(w in t for w in ["probability distribution", "random variable", "normal distribution", "binomial distribution", "chance phenomena", "probability"])
            )
        ),
        "2.B": lambda c, t, o, it: (
            c in ["STAT 121", "ECON 110", "CBE 451", "CBE 311"] and (
                any(w in t for w in ["expected value", "weighted average", "decision making", "decision analysis", "expected monetary value"])
            )
        ),
        "2.C": lambda c, t, o, it: (
            c in ["STAT 121", "CBE 285", "CBE 345", "CBE 385", "CBE 445", "CBE 479"] and (
                any(w in t for w in ["hypothesis test", "design of experiment", "doe", "t-test", "anova", "analysis of variance", "outlier", "p-value", "null hypothesis", "experimentation and analysis"])
            )
        ),
        "2.D": lambda c, t, o, it: (
            c in ["STAT 121", "CBE 285", "CBE 345", "CBE 385", "CBE 445", "CBE 479"] and (
                any(w in t for w in ["central tendenc", "standard deviation", "confidence interval", "dispersion", "mean, mode", "data exploration", "summary statistics", "standard error", "sampling"])
            )
        ),
        "2.E": lambda c, t, o, it: (
            c in ["STAT 121", "CBE 263", "CBE 285", "CBE 345", "CBE 385", "CBE 445", "CBE 479"] and (
                any(w in t for w in ["regression", "curve fit", "least squares", "linear regression", "correlation"])
            )
        ),
        "2.F": lambda c, t, o, it: (
            c in ["STAT 121", "CBE 436", "CBE 451", "CBE 479"] and (
                any(w in t for w in ["statistical control", "control limit", "control chart", "statistical process control", "spc", "process capability", "engineering statistics"])
            )
        ),

        # 3. Engineering Sciences (4-6)
        "3.A": lambda c, t, o, it: (
            (c == "PHSCS 121" and any(w in t for w in ["dynamics", "friction", "force", "acceleration", "momentum", "newton's laws", "mechanics"]))
            or (c == "CBE 374" and any(w in t for w in ["momentum transport", "momentum balances", "drag force", "drag"]))
        ),
        "3.B": lambda c, t, o, it: (
            (c == "PHSCS 121" and any(w in t for w in ["work, energy", "kinetic energy", "potential energy", "conservation laws", "work"]))
            or (c in ["CBE 273", "CBE 374"] and any(w in t for w in ["work of pumps, turbines", "work and unit ops"]))
        ),
        "3.C": lambda c, t, o, it: (
            (c == "PHSCS 121" and any(w in t for w in ["electric", "current", "voltage", "ohm", "kirchhoff", "charge"]))
            or (c in ["CHEM 111", "CHEM 112"] and "electrochemistry" in t)
            or (c == "CBE 378" and any(w in t for w in ["electronic properties", "electronic behavior"]))
            or (c == "CBE 436" and any(w in t for w in ["instrumentation", "transducers", "sensors", "circuit"]))
        ),

        # 4. Materials Science (4-6)
        "4.A": lambda c, t, o, it: (
            c in ["CBE 378", "CBE 345", "CBE 451", "CBE 376"] and (
                any(w in t for w in ["mechanical propert", "mechanical behavior", "stress", "strain", "tensile strength", "yield strength", "failure", "creep", "fatigue", "physical/chemical behaviors of materials", "behaviors of materials"])
            )
        ),
        "4.B": lambda c, t, o, it: (
            c in ["CBE 378", "CBE 345", "CBE 451"] and (
                any(w in t for w in ["material types", "ferrous", "nonferrous", "metals", "alloys", "materials selection", "materials, based on their properties", "engineered materials"])
                or (c == "CBE 378" and "phase diagrams" in t)
            )
        ),
        "4.C": lambda c, t, o, it: (
            c in ["CBE 378", "CBE 451", "CHEM 111"] and (
                any(w in t for w in ["corrosion", "oxidation of metal", "galvanic", "passivation"])
            )
        ),
        "4.D": lambda c, t, o, it: (
            c in ["CBE 378", "CBE 345", "CHEM 357"] and (
                any(w in t for w in ["polymer", "ceramic", "composite", "macromolecul", "glasses"])
            )
        ),

        # 5. Chemistry and Biology (7-11)
        "5.A": lambda c, t, o, it: (
            c in ["CHEM 111", "CHEM 112"] and (
                any(w in t for w in ["inorganic chemistry", "molarity", "normality", "molality", "acids", "bases", "redox", "solubility product", "ph", "periodic table", "electrochemistry", "stoichiometry", "principles of chemistry"])
            )
        ),
        "5.B": lambda c, t, o, it: (
            c in ["CHEM 357", "CBE 345", "CBE 386"] and (
                any(w in t for w in ["organic chemistry", "organic compound", "organic reaction", "conformation", "functional group", "synthesis", "bonding, shape, structure"])
            )
        ),
        "5.C": lambda c, t, o, it: (
            c in ["CHEM 111", "CHEM 112", "CBE 285", "CBE 345", "CBE 385", "CBE 445", "CBE 479"] and (
                any(w in t for w in ["analytical chemistry", "titration", "spectroscopy", "chromatography", "instrumental analysis", "measurement of concentration", "spectrophotomet"])
                or ("process variables" in t and "measurement" in t and "conc" in t)
            )
        ),
        "5.D": lambda c, t, o, it: (
            c in ["BIO 130", "CBE 170", "CBE 273", "CBE 386"] and (
                any(w in t for w in ["biochemistry", "molecular biology", "microbiology", "cell structure", "function of the cell", "krebs", "glycolysis", "calvin", "enzyme", "protein", "genetics", "dna", "biology"])
            )
        ),
        "5.E": lambda c, t, o, it: (
            c in ["CBE 170", "CBE 263", "CBE 273", "CBE 386", "CBE 451", "BIO 130"] and (
                any(w in t for w in ["bioprocess", "fermentation", "biological treatment", "aerobic", "anaerobic", "biological process principles", "bioreactor", "biochemical", "cell growth"])
            )
        ),

        # 6. Fluid Mechanics/Dynamics (8-12)
        "6.A": lambda c, t, o, it: (
            c in ["CBE 374", "CBE 285", "CBE 479"] and (
                any(w in t for w in ["fluid properties", "fluid statics", "viscosity", "shear stress", "hydrostatic", "fluid mechanics"])
            )
        ),
        "6.B": lambda c, t, o, it: (
            c in ["CBE 374", "CBE 285", "CBE 476", "CBE 479"] and (
                any(w in t for w in ["dimensionless number", "reynolds number", "friction factor", "dimensional analysis", "nondimensionalize"])
            )
        ),
        "6.C": lambda c, t, o, it: (
            c in ["CBE 374", "CBE 285", "CBE 451", "CBE 479"] and (
                any(w in t for w in ["mechanical energy balance", "pressure drop", "pressure losses", "flow through pipes", "pipes, valves", "pipe network", "packed bed", "ergun", "flow systems involving pumps, valves, piping", "flow system design"])
            )
        ),
        "6.D": lambda c, t, o, it: (
            c in ["CBE 374", "CBE 285", "CBE 273", "PHSCS 121"] and (
                any(w in t for w in ["bernoulli", "hydrostatic pressure", "velocity head", "fluid statics", "manometer"])
            )
        ),
        "6.E": lambda c, t, o, it: (
            c in ["CBE 374", "CBE 285", "CBE 479"] and (
                any(w in t for w in ["laminar and turbulent", "laminar flow", "turbulent flow", "boundary layer", "boundary-layer", "transition to turbulence"])
            )
        ),
        "6.F": lambda c, t, o, it: (
            c in ["CBE 374", "CBE 285", "CBE 479", "CBE 273", "CBE 345", "CBE 385", "CBE 445"] and (
                any(w in t for w in ["flow measurement", "orifice", "venturi", "rotameter", "flow meter", "pitot"])
                or ("process variables" in t and "flow rate" in t and "measurement" in t)
            )
        ),
        "6.G": lambda c, t, o, it: (
            c in ["CBE 374", "CBE 285", "CBE 273", "CBE 451", "CBE 479"] and (
                any(w in t for w in ["pumps", "turbines", "compressors", "vacuum systems", "pump sizing", "system demand and pump supply curves", "turbines and compressors", "pumps and valves", "perform design calculations for pumps"])
            )
        ),
        "6.H": lambda c, t, o, it: (
            c in ["CBE 374", "CBE 285"] and (
                any(w in t for w in ["compressible flow", "non-newtonian", "mach number", "choked flow", "bingham plastic", "power law fluid"])
            )
        ),

        # 7. Thermodynamics (8-12)
        "7.A": lambda c, t, o, it: (
            c in ["CBE 373", "CBE 273", "CHEM 467", "CHEM 111", "CHEM 112"] and (
                any(w in t for w in ["thermodynamic propert", "internal energy", "enthalpy", "entropy", "free energy", "equations of state", "ideal gas law", "compressibility factor", "volumetric properties"])
            )
        ),
        "7.B": lambda c, t, o, it: (
            c in ["CBE 373", "CBE 273", "CBE 476", "CBE 451", "CHEM 467"] and (
                any(w in t for w in ["phase diagram", "steam table", "psychrometric", "t-s", "p-h", "x-y", "t-x-y", "p-x-y", "bubble point", "dew point", "pure-component phase behavior", "p-v-t"])
            )
        ),
        "7.C": lambda c, t, o, it: (
            c in ["CBE 373", "CBE 273", "CHEM 467"] and (
                any(w in t for w in ["thermodynamic laws", "first law", "second law", "1st law of thermodynamics", "entropy generation", "carnot", "reversibility", "irreversibility"])
            )
        ),
        "7.D": lambda c, t, o, it: (
            c in ["CBE 373", "CBE 273", "CBE 385", "CHEM 467"] and (
                any(w in t for w in ["isothermal", "adiabatic", "isentropic", "phase change", "throttling", "joule-thomson", "latent heat", "thermodynamic analysis of processes"])
            )
        ),
        "7.E": lambda c, t, o, it: (
            c in ["CBE 373", "CBE 385", "CBE 451"] and (
                any(w in t for w in ["power and refrigeration cycles", "refrigeration cycle", "heat pump", "rankine", "brayton", "carnot cycle", "power cycle", "cyclic processes"])
            )
        ),
        "7.F": lambda c, t, o, it: (
            c in ["CBE 373", "CBE 476", "CBE 273", "CBE 451", "CHEM 467"] and (
                any(w in t for w in ["phase equilibrium", "fugacity", "activity coefficient", "raoult's law", "henry's law", "vapor-liquid equilibrium", "vle", "lle", "azeotrope", "solution thermodynamics", "chemical potential", "flash calculation", "physical equilibrium"])
            )
        ),
        "7.G": lambda c, t, o, it: (
            c in ["CBE 373", "CHEM 112", "CHEM 467", "CBE 386", "CBE 273", "CBE 451"] and (
                any(w in t for w in ["chemical equilibrium", "equilibrium constant", "reaction equilibrium", "le chatelier", "extent of reaction at equilibrium", "chemical reaction equilibrium"])
            )
        ),
        "7.H": lambda c, t, o, it: (
            c in ["CBE 273", "CBE 373", "CHEM 111", "CHEM 112", "CHEM 467"] and (
                any(w in t for w in ["heat of reaction", "heat of combustion", "heat of mixing", "enthalpy of reaction", "heat of solution", "excess enthalpy"])
            )
        ),

        # 8. Material/Energy Balances (10-15)
        "8.A": lambda c, t, o, it: (
            c in ["CBE 273", "CBE 170", "CBE 263", "CBE 451", "CBE 476", "CBE 479"] and (
                any(w in t for w in ["steady state material balance", "steady-state mass balance", "material balance", "conservation of mass", "degrees of freedom", "component balance"])
                or (c == "CBE 263" and "process principles" in t)
            )
        ),
        "8.B": lambda c, t, o, it: (
            c in ["CBE 273", "CBE 436", "CBE 386"] and (
                any(w in t for w in ["transient mass balance", "unsteady-state mass balance", "unsteady state material balance", "dynamic mass balance", "accumulation of mass"])
            )
        ),
        "8.C": lambda c, t, o, it: (
            c in ["CBE 273", "CBE 170", "CBE 376", "CBE 451", "CBE 476", "CBE 479"] and (
                any(w in t for w in ["steady state energy balance", "steady-state energy balance", "energy balance", "conservation of energy", "heat balance", "enthalpy balance"])
            )
        ),
        "8.D": lambda c, t, o, it: (
            c in ["CBE 273", "CBE 376", "CBE 436"] and (
                any(w in t for w in ["transient energy balance", "unsteady-state energy balance", "unsteady state energy balance", "dynamic energy balance", "accumulation of energy"])
            )
        ),
        "8.E": lambda c, t, o, it: (
            c in ["CBE 273", "CBE 451"] and (
                any(w in t for w in ["recycle", "bypass", "purge", "multi-unit", "multiple-unit process", "single-pass conversion"])
            )
        ),
        "8.F": lambda c, t, o, it: (
            c in ["CBE 273", "CHEM 111", "CBE 451"] and (
                any(w in t for w in ["material balances with reaction", "reactive system", "combustion", "excess air", "theoretical oxygen", "limiting reactant", "extent of reaction in material balances"])
            )
        ),

        # 9. Heat Transfer (8-12)
        "9.A": lambda c, t, o, it: (
            c in ["CBE 376", "CBE 385", "CBE 479"] and (
                any(w in t for w in ["conductive heat transfer", "conduction", "fourier's law", "thermal conductivity", "thermal resistance", "heat transfer with resistances", "transient heat transfer"])
            )
        ),
        "9.B": lambda c, t, o, it: (
            c in ["CBE 376", "CBE 385", "CBE 479"] and (
                any(w in t for w in ["convective heat transfer", "convection", "natural convection", "forced convection", "nusselt number", "prandtl number", "convective transfer coefficients"])
            )
        ),
        "9.C": lambda c, t, o, it: (
            c in ["CBE 376", "CBE 385"] and (
                any(w in t for w in ["radiation heat transfer", "radiative heat transfer", "radiation", "stefan-boltzmann", "emissivity", "view factor"])
            )
        ),
        "9.D": lambda c, t, o, it: (
            c in ["CBE 376", "CBE 385", "CBE 479"] and (
                any(w in t for w in ["heat-transfer coefficient", "heat transfer coefficient", "convective transfer coefficients", "overall heat transfer coefficient", "fouling", "resistances"])
            )
        ),
        "9.E": lambda c, t, o, it: (
            c in ["CBE 376", "CBE 385", "CBE 451", "CBE 479"] and (
                any(w in t for w in ["heat exchanger", "double pipe", "shell and tube", "shell & tube", "log-mean temperature difference", "lmtd", "heat transfer process units", "design process units for heat transfer"])
            )
        ),

        # 10. Mass Transfer and Separation (8-12)
        "10.A": lambda c, t, o, it: (
            c in ["CBE 376", "CBE 476", "CBE 385"] and (
                any(w in t for w in ["molecular diffusion", "diffusive mass transfer", "diffusion", "fick's law", "diffusivity", "mass flux"])
            )
        ),
        "10.B": lambda c, t, o, it: (
            c in ["CBE 376", "CBE 476", "CBE 385"] and (
                any(w in t for w in ["convective mass transfer", "mass-transfer coefficient", "mass transfer coefficient", "eddy diffusion", "sherwood", "schmidt", "interphase mass transfer", "convective transfer coefficients"])
            )
        ),
        "10.C": lambda c, t, o, it: (
            c in ["CBE 476", "CBE 445", "CBE 451", "CBE 479"] and (
                any(w in t for w in ["separation system", "separation processes", "distillation", "absorption", "extraction", "liquid-liquid extraction", "membrane separation", "adsorption", "stripping", "flash calculations", "separations"])
            )
        ),
        "10.D": lambda c, t, o, it: (
            c in ["CBE 476", "CBE 445", "CBE 479"] and (
                any(w in t for w in ["equilibrium stage", "mccabe-thiele", "tray efficiency", "tray-type column", "number of trays", "batch distillation", "equilibrium-stage"])
            )
        ),
        "10.E": lambda c, t, o, it: (
            c in ["CBE 476", "CBE 445", "CBE 451", "CBE 479"] and (
                any(w in t for w in ["continuous contact", "packed column", "packed tower", "hetp", "htu", "number of transfer units", "packing material", "flooding velocity"])
            )
        ),
        "10.F": lambda c, t, o, it: (
            (c in ["CBE 476", "CBE 479", "CBE 376", "CBE 445"] and any(w in t for w in ["humidification", "drying", "evaporation", "dehumidification", "psychrometry", "mass transfer operations"]))
            or (c == "CBE 273" and "latent heat" in t)
        ),

        # 11. Solids Handling (3-5) - Set to zero as requested (not covered in courses taught)
        "11.A": lambda c, t, o, it: False,
        "11.B": lambda c, t, o, it: False,
        "11.C": lambda c, t, o, it: False,

        # 12. Chemical Reaction Engineering (7-11)
        "12.A": lambda c, t, o, it: (
            c in ["CBE 386", "CBE 345", "CHEM 467", "CHEM 112"] and (
                any(w in t for w in ["reaction rate", "reaction order", "definitions of rate", "forms of rate expressions", "fundamentals of kinetics", "chemical kinetics", "rate equation", "competing reactions kinetics"])
            )
        ),
        "12.B": lambda c, t, o, it: (
            c in ["CBE 386", "CBE 345", "CHEM 467", "CHEM 112"] and (
                any(w in t for w in ["rate constant", "arrhenius", "activation energy", "fundamentals of kinetics", "temperature effects on kinetics"])
            )
        ),
        "12.C": lambda c, t, o, it: (
            c in ["CBE 386", "CBE 273", "CBE 345", "CBE 451"] and (
                any(w in t for w in ["conversion", "yield", "selectivity", "fundamentals of kinetics", "relationships between moles, concentration, extent of reaction and conversion", "conversion, extent of reaction", "extent of reaction in material balances"])
            )
        ),
        "12.D": lambda c, t, o, it: (
            c in ["CBE 386", "CBE 345", "CHEM 467"] and (
                any(w in t for w in ["competing reactions", "series", "parallel", "reversible", "homogeneous", "heterogeneous reaction", "multiple reactions", "biological reactions"])
            )
        ),
        "12.E": lambda c, t, o, it: (
            c in ["CBE 386", "CBE 345", "CBE 451", "CBE 479"] and (
                any(w in t for w in ["reactor design", "reactor types", "batch reactor", "cstr", "continuous stirred tank", "plug flow", "pfr", "ideal reactors", "isothermal and non-isothermal chemical reactors", "design of chemical reactors", "size and do performance calculations on single, isothermal plug-flow, cstr, and batch"])
            )
        ),
        "12.F": lambda c, t, o, it: (
            c in ["CBE 386", "CBE 345", "CHEM 467"] and (
                any(w in t for w in ["catalysis", "catalyst", "catalytic", "biocatalysis", "heterogeneous catalysis", "effectiveness factor"])
            )
        ),

        # 13. Economics (4-6)
        "13.A": lambda c, t, o, it: (
            c in ["CBE 451", "ECON 110", "CBE 461"] and (
                any(w in t for w in ["time value of money", "value of money", "interest, compounding", "present worth", "annual worth", "future worth", "rate of return", "net present value", "npv", "internal rate of return", "irr", "discounted cash flow"])
            )
        ),
        "13.B": lambda c, t, o, it: (
            c in ["ECON 110", "CBE 451", "CBE 461"] and (
                any(w in t for w in ["economic analyses", "break-even", "benefit-cost", "optimal economic life", "profitability", "economic principles", "economic efficiency", "cash flow, and profit"])
            )
        ),
        "13.C": lambda c, t, o, it: (
            c in ["ECON 110", "CBE 451", "CBE 461", "CBE 311"] and (
                any(w in t for w in ["uncertainty", "economic risk", "expected value and risk", "risk management", "sensitivity analysis"])
            )
        ),
        "13.D": lambda c, t, o, it: (
            c in ["CBE 451", "ECON 110", "CBE 461"] and (
                any(w in t for w in ["project selection", "project profitability", "capital ventures", "capital costs, operating costs", "depreciation", "discounted cash flow"])
            )
        ),

        # 14. Process Design (7-11)
        "14.A": lambda c, t, o, it: (
            c in ["CBE 451", "CBE 461", "CBE 170", "CBE 273"] and (
                any(w in t for w in ["process flow diagram", "pfd", "piping and instrumentation", "p&id", "design multiple-unit processes", "flow sheets"])
            )
        ),
        "14.B": lambda c, t, o, it: (
            c in ["CBE 451", "CBE 461", "CBE 374", "CBE 376", "CBE 386", "CBE 476"] and (
                any(w in t for w in ["equipment sizing", "sizing and scale-up", "design flow systems involving pumps", "design separations process units", "design process units for heat transfer", "design shell & tube", "design double pipe", "design isothermal and non-isothermal chemical reactors", "tray-type columns"])
            )
        ),
        "14.C": lambda c, t, o, it: (
            c in ["CBE 451", "CBE 461"] and (
                any(w in t for w in ["capital costs", "estimate costs in capital ventures", "equipment costing", "cost estimation", "cost indices", "capital costs, operating costs"])
            )
        ),
        "14.D": lambda c, t, o, it: (
            c in ["CBE 451", "CBE 461", "CBE 170", "CBE 476"] and (
                any(w in t for w in ["process design", "synthesis and design of chemical", "process simulation software", "multiple-unit process design", "commercial process simulation", "green engineering", "sustainability"])
            )
        ),
        "14.E": lambda c, t, o, it: (
            c in ["CBE 451", "CBE 461", "CBE 311"] and (
                any(w in t for w in ["design standards", "safety and environmental regulations and be able to incorporate safety and environmental considerations into engineering design", "ragagep", "pertinent safety laws and regulations"])
            )
        ),

        # 15. Process Control (4-6)
        "15.A": lambda c, t, o, it: (
            c in ["CBE 436", "CBE 445"] and (
                any(w in t for w in ["first- and second-order dynamic responses", "dynamics", "transfer functions", "stability analysis", "dynamic simulation", "dynamic analysis of open- and closed-loop"])
            )
        ),
        "15.B": lambda c, t, o, it: (
            c in ["CBE 436", "CBE 445"] and (
                any(w in t for w in ["feedback control", "feedforward control", "cascade control", "ratio control", "feedback control loop tuning", "controller tuning", "advanced controllers"])
            )
        ),
        "15.C": lambda c, t, o, it: (
            c in ["CBE 436", "CBE 445"] and (
                any(w in t for w in ["control system instrumentation", "control loop", "control valves", "sensors", "transducers", "measured and manipulated", "plc", "dcs", "interlocks", "process control system"])
            )
        ),

        # 16. Safety, Health, and Environment (5-8)
        "16.A": lambda c, t, o, it: (
            c in ["CBE 311", "CBE 285", "CBE 345", "CBE 385", "CBE 445", "CBE 451", "CBE 479"] and (
                any(w in t for w in ["hazcom", "toxicology", "chemical process safety", "safe laboratory practices", "hazardous properties", "flammability", "toxicity", "safety laws and regulations", "safe engineering practices"])
            )
        ),
        "16.B": lambda c, t, o, it: (
            c in ["CBE 311", "CBE 285", "CBE 345", "CBE 385", "CBE 445", "CBE 479"] and (
                any(w in t for w in ["industrial hygiene", "personal protective equipment", "ppe", "safe laboratory practices", "occupational health", "safe engineering practice", "hazcom"])
            )
        ),
        "16.C": lambda c, t, o, it: (
            c in ["CBE 311", "CBE 451", "CBE 461", "CBE 479"] and (
                any(w in t for w in ["risk management", "hazops", "hazop", "layers of protection analysis (lopa)", "lopa", "fault-tree analyses", "fault tree", "hazard identification", "risk assessment"])
            )
        ),
        "16.D": lambda c, t, o, it: (
            c in ["CBE 311", "CBE 451", "CBE 436", "CBE 479"] and (
                any(w in t for w in ["relief", "overpressure", "pressure relief", "safe engineering practices", "safety considerations are incorporated into engineering design"])
            )
        ),
        "16.E": lambda c, t, o, it: (
            c in ["CBE 311", "CBE 451", "CBE 461"] and (
                any(w in t for w in ["environmental regulations", "safe and environmentally responsible engineering", "waste minimization", "waste treatment", "pollution prevention", "safety and environmental considerations"])
            )
        ),
        "16.F": lambda c, t, o, it: (
            c in ["CBE 311", "CBE 386", "CBE 451"] and (
                any(w in t for w in ["runaway", "reactivity hazards", "inerting", "non-isothermal reactors", "chemical process safety"])
            )
        ),

        # 17. Ethics and Professional Practice (3-5)
        "17.A": lambda c, t, o, it: (
            c in ["CBE 273", "CBE 311", "CBE 451", "CBE 461", "CBE 170", "WRTG 316"] and (
                any(w in t for w in ["aiche code of ethics", "codes of ethics", "making ethical decisions", "ethical and professional responsibilities", "ethics in engineering", "code of ethics"])
                or ("ethics" in o.lower() and c in ["CBE 273", "CBE 311", "WRTG 316"])
            )
        ),
        "17.B": lambda c, t, o, it: (
            c in ["CBE 291", "CBE 391", "CBE 461", "WRTG 316"] and (
                any(w in t for w in ["contract", "nondisclosure", "nda", "agreements", "professional employment"])
            )
        ),
        "17.C": lambda c, t, o, it: (
            c in ["CBE 170", "CBE 191", "CBE 273", "CBE 374", "CBE 378", "CBE 451", "CBE 461", "CBE 476", "CBE 311", "WRTG 316"] and (
                any(w in t for w in ["public health, safety, and welfare", "global impact of chem", "global, cultural, social, environmental, and economic factors"])
            )
        ),
        "17.D": lambda c, t, o, it: (
            c in ["CBE 451", "CBE 461", "CBE 291", "CBE 391", "WRTG 316"] and (
                any(w in t for w in ["intellectual property", "patent", "copyright", "ethically incorporating research", "trade secrets", "information literacy"])
            )
        )
    }
    return rules
