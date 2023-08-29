from aiida.plugins import WorkflowFactory
from aiida import engine, orm

RelaxWorkChain = WorkflowFactory('common_workflows.relax.cp2k')



structure = load_node(1559)  # A `StructureData` node representing the structure to be optimized.
engines = {
    'relax': {
        'code': orm.load_code('cp2k.main@local_slurm') ,  # An identifier of a `Code` configured for the `quantumespresso.pw` plugin
        'options': {
            'resources': {
                'num_machines': 1,  # Number of machines/nodes to use
            },
            'max_wallclock_seconds': 3600,  # Number of wallclock seconds to request from thescheduler for each job
        }
    }
}

builder = RelaxWorkChain.get_input_generator().get_builder(structure=structure, engines=engines, protocol='test')
engine.run(builder)
