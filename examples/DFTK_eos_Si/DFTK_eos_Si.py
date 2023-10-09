from aiida import engine, orm
from aiida.plugins import WorkflowFactory
from aiida.orm import List
from aiida_common_workflows.common import ElectronicType, RelaxType



code = orm.load_code('dftk@jed_on_scitas') 

#load silicon structure
cif = orm.CifData(file="/home/yiwu/source/aiida-common-workflows/examples/DFTK_eos_Si/Si_primitive.cif")
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
            'max_wallclock_seconds': 7200,  # Number of wallclock seconds to request from the scheduler for each job
            'max_memory_kb': 344064000,
            'queue_name': 'bigmem'
        }
    }
}



cls = WorkflowFactory('common_workflows.eos')

#electronic_type: default is 'METAL', AUTOMATIC: follow protocol or UNKOWN, INSULATOR: fixed occupation, METAL: cold smearing, UNKNOWN: gaussian smearing
#relax_type: currently only support NONE: no relaxation
inputs = {
    'structure': structure,
    'scale_factors': List(list=[1, 1, 1]),
    'generator_inputs': {  # code-agnostic inputs for the relaxation
        'engines': engines,
        'protocol': 'verification-pbe-v1',
        'relax_type': RelaxType.NONE,
        'electronic_type': ElectronicType.AUTOMATIC
    },
    'sub_process_class': 'common_workflows.relax.dftk'
}

engine.submit(cls, **inputs)