"""
Thermodynamic property calculations using CoolProp.
"""
import CoolProp.CoolProp as CP
from typing import Dict, Optional

class PropertyCalculator:
    """Calculate thermodynamic properties for various fluids."""
    
    FLUID_MAP = {
        'water': 'Water',
        'air': 'Air',
        'r134a': 'R134a',
        'r22': 'R22',
        'co2': 'CO2'
    }
    
    def __init__(self, fluid: str):
        """Initialize calculator for a specific fluid."""
        if fluid.lower() not in self.FLUID_MAP:
            raise ValueError(f"Unsupported fluid: {fluid}")
        self.fluid = self.FLUID_MAP[fluid.lower()]
    
    def get_properties(self, **kwargs) -> Dict[str, float]:
        """
        Get thermodynamic properties given two independent properties.
        
        Supported input combinations:
        - temp + pressure
        - temp + quality (for two-phase)
        - pressure + enthalpy
        - pressure + entropy
        - enthalpy + entropy
        """
        try:
            # Convert inputs and determine state
            if 'temp' in kwargs and 'pressure' in kwargs:
                T = float(kwargs['temp']) + 273.15  # Convert C to K
                P = float(kwargs['pressure']) * 1000  # Convert kPa to Pa
                
            elif 'temp' in kwargs and 'quality' in kwargs:
                T = float(kwargs['temp']) + 273.15
                Q = float(kwargs['quality'])
                P = CP.PropsSI('P', 'T', T, 'Q', Q, self.fluid)
                
            elif 'pressure' in kwargs and 'enthalpy' in kwargs:
                P = float(kwargs['pressure']) * 1000
                H = float(kwargs['enthalpy']) * 1000  # kJ/kg to J/kg
                T = CP.PropsSI('T', 'P', P, 'H', H, self.fluid)
                
            elif 'pressure' in kwargs and 'entropy' in kwargs:
                P = float(kwargs['pressure']) * 1000
                S = float(kwargs['entropy']) * 1000
                T = CP.PropsSI('T', 'P', P, 'S', S, self.fluid)
                
            elif 'enthalpy' in kwargs and 'entropy' in kwargs:
                H = float(kwargs['enthalpy']) * 1000
                S = float(kwargs['entropy']) * 1000
                T = CP.PropsSI('T', 'H', H, 'S', S, self.fluid)
                P = CP.PropsSI('P', 'H', H, 'S', S, self.fluid)
            else:
                raise ValueError("Must provide two independent properties (temp+pressure, temp+quality, etc.)")
            
            # Calculate all properties using the determined T and P
            props = {}
            props['temperature'] = T - 273.15
            props['pressure'] = P / 1000
            props['enthalpy'] = CP.PropsSI('H', 'T', T, 'P', P, self.fluid) / 1000
            props['entropy'] = CP.PropsSI('S', 'T', T, 'P', P, self.fluid) / 1000
            props['density'] = CP.PropsSI('D', 'T', T, 'P', P, self.fluid)
            props['specific_volume'] = 1.0 / props['density']
            props['internal_energy'] = CP.PropsSI('U', 'T', T, 'P', P, self.fluid) / 1000
            
            # Try to get quality (will be -1 for single phase)
            try:
                quality = CP.PropsSI('Q', 'T', T, 'P', P, self.fluid)
                if 0 <= quality <= 1:
                    props['quality'] = quality
                else:
                    props['quality'] = None
            except:
                props['quality'] = None
            
            return props
            
        except Exception as e:
            raise ValueError(f"Error calculating properties: {str(e)}")
    
    def get_saturation_properties(self, temp: Optional[float] = None, 
                                  pressure: Optional[float] = None) -> Dict[str, float]:
        """Get saturation properties at given temperature or pressure."""
        if temp is not None:
            T = float(temp) + 273.15
            P = CP.PropsSI('P', 'T', T, 'Q', 0, self.fluid)
        elif pressure is not None:
            P = float(pressure) * 1000
            T = CP.PropsSI('T', 'P', P, 'Q', 0, self.fluid)
        else:
            raise ValueError("Must specify either temperature or pressure")
        
        props = {}
        props['temperature'] = T - 273.15
        props['pressure'] = P / 1000
        
        # Saturated liquid properties (Q=0)
        props['h_f'] = CP.PropsSI('H', 'P', P, 'Q', 0, self.fluid) / 1000
        props['s_f'] = CP.PropsSI('S', 'P', P, 'Q', 0, self.fluid) / 1000
        props['v_f'] = 1.0 / CP.PropsSI('D', 'P', P, 'Q', 0, self.fluid)
        
        # Saturated vapor properties (Q=1)
        props['h_g'] = CP.PropsSI('H', 'P', P, 'Q', 1, self.fluid) / 1000
        props['s_g'] = CP.PropsSI('S', 'P', P, 'Q', 1, self.fluid) / 1000
        props['v_g'] = 1.0 / CP.PropsSI('D', 'P', P, 'Q', 1, self.fluid)
        
        # Latent heat
        props['h_fg'] = props['h_g'] - props['h_f']
        props['s_fg'] = props['s_g'] - props['s_f']
        
        return props
