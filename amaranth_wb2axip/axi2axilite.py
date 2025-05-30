#

from amaranth import Instance, ClockSignal, ResetSignal, Module
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from .interfaces import AXI4, AXI4Lite
from .utils import add_verilog_file


class AXI2AXILite(wiring.Component):
    DEPENDENCIES = ['axi2axilite.v', 'skidbuffer.v', 'axi_addr.v', 'sfifo.v']

    def __init__(self, data_w, addr_w, id_w, domain='sync'):
        self.data_w = data_w
        self.addr_w = addr_w
        self.id_w = id_w
        self.domain = domain
        super().__init__({
            'axilite': Out(AXI4Lite(data_w, addr_w)),
            'axi': In(AXI4(data_w, addr_w, id_w)),
        })

    def elaborate(self, platform):
        m = Module()
        m.submodules.axi2axil_i = Instance(
            'axi2axilite',
            p_C_AXI_ID_WIDTH=self.id_w,
            p_C_AXI_DATA_WIDTH=self.data_w,
            p_C_AXI_ADDR_WIDTH=self.addr_w,
            i_S_AXI_ACLK=ClockSignal(self.domain),
            i_S_AXI_ARESETN=~ResetSignal(self.domain),
            **self.axi.get_ports_for_instance(prefix='S_AXI_'),
            **self.axilite.get_ports_for_instance(prefix='M_AXI_'),
        )
        if platform is not None:
            for d in self.DEPENDENCIES:
                add_verilog_file(platform, d)
        return m


if __name__ == '__main__':
    from amaranth.cli import main
    core = AXI2AXILite(32, 8, 5)
    main(core, None, ports=core.axi.all_ports + core.axilite.all_ports)
