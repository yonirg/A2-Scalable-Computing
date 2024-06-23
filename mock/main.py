from graph_user_flow import *
import simulation


if __name__ == "__main__":
    print("Starting simulation...")

    params = simulation.SimulationParams(
        cycle_duration=0.1,
        num_initial_users=1010,
        num_initial_products=200,
        num_initial_stores=5,
        qtd_stock_initial=2000,
        max_simultaneus_users=1000,
        num_new_users_per_cycle=100,
        num_new_products_per_cycle=20,
    )

    sim = simulation.Simulation(params)
    sim.run()

    print("Simulation finished.")
