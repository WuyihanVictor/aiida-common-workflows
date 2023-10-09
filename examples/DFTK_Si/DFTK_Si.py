from aiida import engine, orm
from aiida.plugins import WorkflowFactory
from aiida_common_workflows.common import ElectronicType



code = orm.load_code('dftk@jed_on_scitas') 

#load silicon structure
cif = orm.CifData(file="/home/yiwu/source/aiida-common-workflows/examples/DFTK_Si/Si_primitive.cif")
structure = cif.get_structure()



RelaxWorkChain = WorkflowFactory('common_workflows.relax.dftk')  # Load the relax workflow implementation of choice.

structure = structure # A `StructureData` node representing the structure to be optimized.
engines = {
    'relax': {
        'code': code,  # An identifier of a `Code` configured for the `quantumespresso.pw` plugin
        'options': {
            'withmpi': True,
            'resources': {
                'num_machines': 1,  # Number of machines/nodes to use
                'num_mpiprocs_per_machine': 24,
            },
            'max_wallclock_seconds': 3600, # Number of wallclock seconds to request from the scheduler for each job
            'max_memory_kb': 344064000,
            'queue_name': 'bigmem'
        }
    }
}

#electronic_type: default is 'METAL', AUTOMATIC: follow protocol or UNKOWN, INSULATOR: fixed occupation, METAL: cold smearing, UNKNOWN: gaussian smearing
builder = RelaxWorkChain.get_input_generator().get_builder(structure=structure, engines=engines, protocol='verification-pbe-v1',electronic_type=ElectronicType.AUTOMATIC)
engine.submit(builder)
