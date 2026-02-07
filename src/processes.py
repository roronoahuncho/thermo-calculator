"""
Thermodynamic process calculations.
"""
from src.properties import PropertyCalculator
from typing import Dict
import math

class ProcessAnalyzer:
    """Analyze various thermodynamic processes."""
    
    def __init__(self, fluid: str):
        self.calc = PropertyCalculator(fluid)
        self.fluid = fluid
    
    def isentropic_process(self, inlet_temp: float, inlet_pressure: float,
                          outlet_pressure: float, efficiency: float = 1.0,
                          process_type: str = 'compression') -> Dict:
        """
        Analyze isentropic compression or expansion process.
        
        Args:
            inlet_temp: Inlet temperature (C)
            inlet_pressure: Inlet pressure (kPa)
            outlet_pressure: Outlet pressure (kPa)
            efficiency: Isentropic efficiency (0-1)
            process_type: 'compression' or 'expansion'
        """
        # Get inlet properties
        inlet = self.calc.get_properties(temp=inlet_temp, pressure=inlet_pressure)
        
        # Isentropic outlet (same entropy)
        outlet_s = self.calc.get_properties(pressure=outlet_pressure, entropy=inlet['entropy'])
        
        # Actual outlet accounting for efficiency
        if process_type == 'compression':
            h_actual = inlet['enthalpy'] + (outlet_s['enthalpy'] - inlet['enthalpy']) / efficiency
        else:  # expansion
            h_actual = inlet['enthalpy'] - (inlet['enthalpy'] - outlet_s['enthalpy']) * efficiency
        
        outlet_actual = self.calc.get_properties(pressure=outlet_pressure, enthalpy=h_actual)
        
        # Calculate work
        work = outlet_actual['enthalpy'] - inlet['enthalpy']  # kJ/kg
        
        return {
            'inlet': inlet,
            'outlet_isentropic': outlet_s,
            'outlet_actual': outlet_actual,
            'work': work,
            'efficiency': efficiency,
            'process_type': process_type
        }
    
    def isobaric_process(self, inlet_temp: float, pressure: float,
                        outlet_temp: float) -> Dict:
        """Constant pressure heating/cooling process."""
        inlet = self.calc.get_properties(temp=inlet_temp, pressure=pressure)
        outlet = self.calc.get_properties(temp=outlet_temp, pressure=pressure)
        
        heat = outlet['enthalpy'] - inlet['enthalpy']  # kJ/kg
        
        return {
            'inlet': inlet,
            'outlet': outlet,
            'heat_transfer': heat,
            'pressure': pressure
        }
    
    def isochoric_process(self, inlet_temp: float, inlet_pressure: float,
                         outlet_temp: float) -> Dict:
        """Constant volume heating/cooling process."""
        inlet = self.calc.get_properties(temp=inlet_temp, pressure=inlet_pressure)
        
        # For constant volume, find outlet pressure
        # This is approximate for real gases
        outlet_pressure = inlet_pressure * (outlet_temp + 273.15) / (inlet_temp + 273.15)
        outlet = self.calc.get_properties(temp=outlet_temp, pressure=outlet_pressure)
        
        heat = outlet['internal_energy'] - inlet['internal_energy']
        
        return {
            'inlet': inlet,
            'outlet': outlet,
            'heat_transfer': heat,
            'specific_volume': inlet['specific_volume']
        }
    
    def throttling_process(self, inlet_temp: float, inlet_pressure: float,
                          outlet_pressure: float) -> Dict:
        """Isenthalpic throttling process (valve, expansion device)."""
        inlet = self.calc.get_properties(temp=inlet_temp, pressure=inlet_pressure)
        
        # Constant enthalpy
        outlet = self.calc.get_properties(pressure=outlet_pressure, enthalpy=inlet['enthalpy'])
        
        temp_drop = inlet['temperature'] - outlet['temperature']
        
        return {
            'inlet': inlet,
            'outlet': outlet,
            'temperature_drop': temp_drop,
            'enthalpy': inlet['enthalpy']
        }
    
    def polytropic_process(self, inlet_temp: float, inlet_pressure: float,
                          outlet_pressure: float, n: float) -> Dict:
        """
        Polytropic process: PV^n = constant
        
        Args:
            n: Polytropic index (1=isothermal, k=isentropic)
        """
        inlet = self.calc.get_properties(temp=inlet_temp, pressure=inlet_pressure)
        
        # For ideal gas approximation
        T_ratio = (outlet_pressure / inlet_pressure) ** ((n - 1) / n)
        outlet_temp = (inlet_temp + 273.15) * T_ratio - 273.15
        
        outlet = self.calc.get_properties(temp=outlet_temp, pressure=outlet_pressure)
        
        # Work calculation (approximate)
        if abs(n - 1.0) < 0.001:
            # Isothermal
            work = inlet_pressure * inlet['specific_volume'] * math.log(outlet_pressure / inlet_pressure)
        else:
            work = (n / (n - 1)) * (outlet_pressure * outlet['specific_volume'] - 
                                   inlet_pressure * inlet['specific_volume'])
        
        return {
            'inlet': inlet,
            'outlet': outlet,
            'work': work,
            'polytropic_index': n
        }
