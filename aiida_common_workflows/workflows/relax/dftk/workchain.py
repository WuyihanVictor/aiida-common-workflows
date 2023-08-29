# -*- coding: utf-8 -*-
"""Implementation of `aiida_common_workflows.common.relax.workchain.CommonRelaxWorkChain` for Dftk."""
from aiida import orm
from aiida.common import exceptions
from aiida.engine import calcfunction
from aiida_dftk.workflows.base import DftkBaseWorkChain
import numpy as np

from ..workchain import CommonRelaxWorkChain
from .generator import DftkCommonRelaxInputGenerator

__all__ = ('DftkCommonRelaxWorkChain',)


@calcfunction
def get_stress(parameters):
    """Return the stress array from the given parameters node."""
    stress = orm.ArrayData()
    stress.set_array(name='stress', array=np.array(parameters.get_array(name='output_stresses')))
    return stress


@calcfunction
def get_forces(parameters):
    """Return the forces array from the given parameters node."""
    forces = orm.ArrayData()
    forces.set_array(name='forces', array=np.array(parameters.get_array(name='output_forces')))
    return forces


@calcfunction
def get_total_energy(parameters):
    """Return the total energy from the given parameters node."""
    return orm.Float(parameters.get_dict()['energies']['total'])


# @calcfunction
# def get_total_magnetization(parameters):
#     """Return the total magnetization from the given parameters node."""
#     return orm.Float(parameters['total_magnetization'])


class DftkCommonRelaxWorkChain(CommonRelaxWorkChain):
    """Implementation of `aiida_common_workflows.common.relax.workchain.CommonRelaxWorkChain` for Dftk."""

    _process_class = DftkBaseWorkChain
    _generator_class = DftkCommonRelaxInputGenerator

    def convert_outputs(self):
        """Convert the outputs of the sub workchain to the common output specification."""
        # TODO: after implementing relax in DFTK
        # try:
        #     self.out('relaxed_structure', self.ctx.workchain.outputs.output_structure)
        # except exceptions.NotExistentAttributeError:
        #     pass

        self.out('total_energy', get_total_energy(self.ctx.workchain.outputs.output_parameters))
        self.out('forces', get_forces(self.ctx.workchain.outputs.output_forces))
        self.out('stress', get_stress(self.ctx.workchain.outputs.output_stresses))

        # TODO: after implementing spin in aiida
        # try:
        #     self.out('total_magnetization', get_total_magnetization(self.ctx.workchain.outputs.output_parameters))
        # except KeyError:
        #     pass
