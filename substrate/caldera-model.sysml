// SYNTHETIC out-of-distribution probe model. "Caldera-2" is a FICTIONAL
// suborbital cargo hopper authored 2026-06-10 for this probe; every value is
// invented. No training corpus contains this vehicle. Structure mirrors the
// Apollo excerpt's shape (engine def, stage def, count requirement, minimum
// thrust requirement, no linking derivation).

package CalderaTechnicalComponents {
	abstract part def RocketEngine :> HardwareComponent {
		attribute thrustSeaLevel :> ISQ::force;
	}
	abstract part def RocketStage :> HardwareComponent {
		part engines[1..*] ordered : RocketEngine;
	}
	part def 'K-9' :> RocketEngine {
		doc /* Pressure-fed methalox engine developed for the Caldera-2 boost stage. */
		attribute thrustSeaLevel = 412 ['kN'];
		attribute specificImpulseSeaLevel = 287 ['s'];
	}
	part def 'C2-Boost' :> RocketStage {
		doc /* The Caldera-2 boost stage, providing all ascent thrust for the hop profile. */
		attribute propellantMass = 18400 [kg];
		attribute dryMass = 2630 [kg];
		part engine1 : 'K-9';
		part engine2 : 'K-9';
		part engine3 : 'K-9';
		part :>> engines[3] = (engine1, engine2, engine3);
	}
}

package CalderaRequirements {
	requirement def <'CL-R2'> BoostEngineConfiguration {
		doc /* The Caldera-2 boost stage shall incorporate three K-9 engines. */
		@Rationale {
			text = "This configuration is required to generate the necessary thrust for pad departure with the full cargo manifest.";
		}
	}
	requirement def <'CL-R7'> BoostThrustMagnitude {
		doc /* The Caldera-2 boost stage propulsion shall provide a minimum thrust of 1.4 Meganewtons at liftoff. */
		@Rationale {
			text = "Sufficient thrust from the boost stage is fundamental to overcome gravity and clear the pad envelope.";
		}
		attribute actualLiftoffThrust :> ISQ::force;
		attribute minLiftoffThrust :> ISQ::force = 1.4 [MN];
		require constraint { actualLiftoffThrust >= minLiftoffThrust }
	}
}
