// EXCERPT of the Airbus Apollo 11 SysML v2 model (MPL-2.0)
// Source: https://github.com/airbus/apollo-11-sysml-v2 @ 6e9c93fe7d80c5ca3534bb14b10ab374a643ef2d
// Extraction criteria: every element bearing on S-IC first-stage propulsion
// (engine defs, stage defs, vehicle assembly, thrust requirements) plus the
// refinement targets of those requirements. Verbatim; comments added only in
// this header. Assembled 2026-06-10 for the consumption probe.

// ---- from Technical/TechnicalComponentsPackage.sysml ----
	abstract part def RocketEngine :> HardwareComponent {
		doc /* An abstract representation of a rocket engine, defining its core performance attributes. */
		attribute thrustVacuum :> ISQ::force;
		attribute specificImpulseVacuum :> CoSMAQuantitiesAndUnitsPackage::specificImpulse;
	}
	abstract part def RocketStage :> FuelledComponent {
		doc /* An abstract representation of a single stage of a rocket, containing engines and propellant. */
		part engines[1..*] ordered : RocketEngine;
	}
	part def SaturnV :> MultistageRocket, LaunchSystem {
		doc /* The three-stage, super heavy-lift launch vehicle used to send the Apollo spacecraft to the Moon. */
		attribute height :> ISQ::length = 110.6 [m];
		attribute launchMass :> ISQ::mass = 2970000 [kg];
		attribute payloadToLunarTransferOrbit :> ISQ::mass = 43500 [kg];
	   
		part stage1 : 'S-IC';
		part stage2 : 'S-II';
		part stage3 : 'S-IVB';
		part instrumentUnit : SaturnVInstrumentUnit;
		part :>> stages[3] = (stage1, stage2, stage3);

		interface stage1ToStage2 : StagingInterface connect stage1.upperStagePort to stage2.lowerStagePort;
		interface stage2ToStage3 : StagingInterface connect stage2.upperStagePort to  stage3.lowerStagePort;
		interface iuToStage3 : GuidanceInterface connect instrumentUnit.stageControlPort to stage3.controlPort;
	}
	part def 'F-1' :> RocketEngine {
		doc /* A single-chamber liquid-propellant rocket engine, the most powerful ever built, used in the S-IC first stage. */
		attribute thrustSeaLevel :> ISQ::force = 6770 ['kN'];
		attribute :>> thrustVacuum = 7770 ['kN'];
		attribute :>> specificImpulseVacuum = 304 ['s'];
	}
	part def 'J-2' :> RocketEngine {
		doc /* A liquid-fuel cryogenic rocket engine used in the S-II and S-IVB stages, notable for its restart capability. */
		attribute :>> thrustVacuum = 1033 ['kN'];
		attribute :>> specificImpulseVacuum = 421 ['s'];
	}
	part def 'S-II' :> RocketStage {
		doc /* The second stage of the Saturn V, providing massive thrust in the upper atmosphere and vacuum of space. */
		attribute :>> propellantMass = 443000 [SI::kg];
		attribute :>> dryMass = 36200 [kg];
		
		port lowerStagePort : ~StagingPort;
		port upperStagePort : StagingPort;
		
		part engine1 : 'J-2';
		part engine2 : 'J-2';
		part engine3 : 'J-2';
		part engine4 : 'J-2';
		part engine5 : 'J-2';
		part :>> engines[5] = (engine1, engine2, engine3, engine4, engine5);
	}
	part def 'S-IC' :> RocketStage {
		doc /* The first stage of the Saturn V, providing the initial ~7.7 million pounds of thrust for liftoff. */
		attribute :>> propellantMass = 2077000 [kg];
		attribute :>> dryMass = 137000 [kg];
	   
		port upperStagePort : StagingPort;
		
		part engine1 : 'F-1';
		part engine2 : 'F-1';
		part engine3 : 'F-1';
		part engine4 : 'F-1';
		part engine5 : 'F-1';
		part :>> engines[5] = (engine1, engine2, engine3, engine4, engine5);
	}

// ---- from Requirements/TechnicalRequirementsPackage.sysml ----
	requirement def <'CLR-R001'> SICEngineConfiguration {
		doc /* The S-IC stage shall incorporate five F-1 engines. */
		@Rationale {
			text = "This configuration is required to generate the necessary thrust to lift the massive Saturn V vehicle off the launch pad.";
		}
		#refinement dependency SICEngineConfiguration to FunctionalRequirementsPackage::'FLR-R008';
	}
	requirement def <'CLR-R002'> SICPropellantCompatibility {
		doc /* The S-IC stage shall be designed to store and deliver RP-1 (Kerosene) and Liquid Oxygen (LOX) to its engines. */
		@Rationale {
			text = "The choice of the F-1 engine dictates the required propellant types for the first stage.";
		}
		#refinement dependency SICPropellantCompatibility to FunctionalRequirementsPackage::'FLR-R001';
	}
	requirement def <'CLR-R055'> SICThrustMagnitude {
		doc /* The Apollo 11 Mission's launch vehicle's first stage propulsion shall provide a minimum thrust of 34.5 Meganewtons at liftoff. */
		@Rationale {
			text = "Sufficient thrust from the first stage is fundamental to overcome Earth's gravity and initiate the launch sequence, enabling the entire mission.";
		}

		attribute actualLiftoffThrust :> ISQ::force;
		attribute minLiftoffThrust :> ISQ::force = 34.5 [MN];

		require constraint { actualLiftoffThrust >= minLiftoffThrust }
	
	}

// ---- from Requirements/FunctionalRequirementsPackage.sysml ----
	requirement def <'FLR-R008'> Stage1ThrustMagnitudeRequirement {
		doc /* The system shall generate a propulsive force from the first stage that results in a positive vertical acceleration at liftoff. */
		@Rationale {
			 text = "A thrust-to-weight ratio greater than one is the fundamental condition required to overcome gravity and lift the vehicle off the launch pad.";
		}
		#refinement dependency 'FLR-R008' to MissionRequirementsPackage::'HLR-R062';
	}

// ---- from Requirements/MissionRequirementsPackage.sysml ----
    requirement def <'HLR-R062'> MechanicalLoadResilience {
        doc /* All primary structures shall withstand the flight environment without compromising 
               mission functionality. */
        @Rationale {
            text = "The spacecraft must survive extreme mechanical stresses during launch and reentry to protect internal subsystems.";
        }
        #refinement dependency 'HLR-R062' to CapabilitiesPackage::HeavyLiftLaunch;
    }
