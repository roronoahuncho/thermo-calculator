"""
Command-line interface for the thermodynamic calculator.
"""
import click
from src.properties import PropertyCalculator
from src.processes import ProcessAnalyzer
from tabulate import tabulate

@click.group()
def cli():
    """Thermodynamic Property & Process Calculator"""
    pass

@cli.command()
@click.option('--fluid', required=True, help='Fluid: water, air, r134a, r22, co2')
@click.option('--temp', type=float, help='Temperature (C)')
@click.option('--pressure', type=float, help='Pressure (kPa)')
@click.option('--quality', type=float, help='Quality (0-1 for two-phase)')
@click.option('--enthalpy', type=float, help='Enthalpy (kJ/kg)')
@click.option('--entropy', type=float, help='Entropy (kJ/kg-K)')
def property(fluid, temp, pressure, quality, enthalpy, entropy):
    """Calculate thermodynamic properties"""
    try:
        calc = PropertyCalculator(fluid)
        
        # Build kwargs from provided options
        kwargs = {}
        if temp is not None:
            kwargs['temp'] = temp
        if pressure is not None:
            kwargs['pressure'] = pressure
        if quality is not None:
            kwargs['quality'] = quality
        if enthalpy is not None:
            kwargs['enthalpy'] = enthalpy
        if entropy is not None:
            kwargs['entropy'] = entropy
        
        props = calc.get_properties(**kwargs)
        
        # Display results
        table = []
        table.append(['Temperature', f"{props['temperature']:.2f}", 'C'])
        table.append(['Pressure', f"{props['pressure']:.2f}", 'kPa'])
        table.append(['Enthalpy', f"{props['enthalpy']:.2f}", 'kJ/kg'])
        table.append(['Entropy', f"{props['entropy']:.4f}", 'kJ/kg-K'])
        table.append(['Specific Volume', f"{props['specific_volume']:.6f}", 'm³/kg'])
        table.append(['Density', f"{props['density']:.2f}", 'kg/m³'])
        table.append(['Internal Energy', f"{props['internal_energy']:.2f}", 'kJ/kg'])
        if props['quality'] is not None:
            table.append(['Quality', f"{props['quality']:.4f}", '-'])
        
        click.echo(f"\n{fluid.upper()} Properties:")
        click.echo(tabulate(table, headers=['Property', 'Value', 'Unit'], tablefmt='grid'))
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--fluid', required=True)
@click.option('--inlet-temp', type=float, required=True)
@click.option('--inlet-pressure', type=float, required=True)
@click.option('--outlet-pressure', type=float, required=True)
@click.option('--efficiency', type=float, default=1.0)
def process(fluid, inlet_temp, inlet_pressure, outlet_pressure, efficiency):
    """Analyze isentropic process"""
    try:
        analyzer = ProcessAnalyzer(fluid)
        
        process_type = 'compression' if outlet_pressure > inlet_pressure else 'expansion'
        result = analyzer.isentropic_process(
            inlet_temp, inlet_pressure, outlet_pressure, efficiency, process_type
        )
        
        click.echo(f"\nIsentropic {process_type.capitalize()} Analysis:")
        click.echo(f"Efficiency: {efficiency*100:.1f}%")
        click.echo(f"Work: {result['work']:.2f} kJ/kg")
        click.echo(f"\nInlet Temperature: {result['inlet']['temperature']:.2f} C")
        click.echo(f"Outlet Temperature (actual): {result['outlet_actual']['temperature']:.2f} C")
        click.echo(f"Outlet Temperature (isentropic): {result['outlet_isentropic']['temperature']:.2f} C")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
def interactive():
    """Interactive mode for property calculations"""
    click.echo("\n=== Thermodynamic Calculator - Interactive Mode ===\n")
    
    fluid = click.prompt('Select fluid', type=click.Choice(['water', 'air', 'r134a', 'r22', 'co2']))
    temp = click.prompt('Temperature (C)', type=float)
    pressure = click.prompt('Pressure (kPa)', type=float)
    
    try:
        calc = PropertyCalculator(fluid)
        props = calc.get_properties(temp=temp, pressure=pressure)
        
        table = []
        for key, value in props.items():
            if value is not None:
                if isinstance(value, float):
                    table.append([key.replace('_', ' ').title(), f"{value:.4f}"])
        
        click.echo(f"\nResults for {fluid.upper()}:")
        click.echo(tabulate(table, headers=['Property', 'Value'], tablefmt='grid'))
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli()
