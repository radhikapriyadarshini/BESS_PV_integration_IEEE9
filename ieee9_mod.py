import pandapower.networks as pn
import pandapower as pp

def modified_ieee9(P_dg, q_dg=0.0, bus_id=5, run_powerflow=True, controllable=False, verbose=False):
    """
    Modifies the IEEE 9-bus system by injecting PV+BESS as a static generator.

    Parameters:
    - P_dg (float): Active power from PV+BESS in MW
    - q_dg (float): Reactive power (default 0.0 Mvar)
    - bus_id (int): Bus number to inject power (default Bus 5)
    - run_powerflow (bool): Whether to run load flow after adding the generator
    - controllable (bool): Whether the generator is controllable (useful for OPF)
    - verbose (bool): If True, prints key bus and line results

    Returns:
    - net: Modified pandapower network object (IEEE 9-bus + PV+BESS)
    """
    # Load IEEE 9-bus system
    net = pn.case9()

    # Add static generator (PV + BESS)
    pp.create_sgen(net,
                   bus=bus_id,
                   p_mw=P_dg,
                   q_mvar=q_dg,
                   name="PV+BESS",
                   controllable=controllable)

    # Run power flow
    if run_powerflow:
        try:
            pp.runpp(net)
            if verbose:
                print("\n=== Bus Voltages ===")
                print(net.res_bus[["vm_pu", "va_degree"]])

                print("\n=== Line Loadings ===")
                print(net.res_line[["loading_percent"]])
        except Exception as e:
            print(f"[ERROR] Power flow did not converge: {e}")

    return net
