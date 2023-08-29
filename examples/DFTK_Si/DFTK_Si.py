from aiida import engine, orm
from aiida.plugins import CalculationFactory

from aiida.plugins import WorkflowFactory



code = orm.load_code('DFTK@local_direct') 

#load silicon structure
cif = orm.CifData(file="/home/max/Desktop/Aiida_DFTK_Test/common_workflow/aiida-common-workflows/examples/DFTK_Si/Si.cif")
structure = cif.get_structure()



RelaxWorkChain = WorkflowFactory('common_workflows.relax.dftk')  # Load the relax workflow implementation of choice.

structure = structure # A `StructureData` node representing the structure to be optimized.
engines = {
    'relax': {
        'code': code,  # An identifier of a `Code` configured for the `quantumespresso.pw` plugin
        'options': {
            'withmpi': False,
            'resources': {
                'num_machines': 1,  # Number of machines/nodes to use
                'num_mpiprocs_per_machine': 1,
            },
            'max_wallclock_seconds': 3600,  # Number of wallclock seconds to request from the scheduler for each job
        }
    }
}

builder = RelaxWorkChain.get_input_generator().get_builder(structure=structure, engines=engines, protocol='fastest')
engine.run(builder)
