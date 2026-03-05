from engine.alignment_engine import AlignmentEngine


def main():

    engine = AlignmentEngine()

    engine.run_simulation(
        num_steps=200,
        shocks={
            60: "DISINFO_BURST",
            120: "RESOURCE_CRUNCH"
        },
        seed=42,
        verbose=True
    )

    print("Simulation complete")
    print("Final S_hat:", engine.x[0])
    print("Final D_hat:", engine.x[1])


if __name__ == "__main__":
    main()