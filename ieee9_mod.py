import pandapower.networks as pn
import pandapower as pp

def modified_ieee9(P_dg, bus_id=5):
    net = pn.case9()
    # Add PV + BESS system as a static generator
    pp.create_sgen(net, bus=bus_id, p_mw=P_dg, q_mvar=0.0, name="PV+BESS")
    return net
