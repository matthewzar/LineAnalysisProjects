using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using log4net;
using SharpNeat.Core;
using SharpNeat.Decoders;
using SharpNeat.Decoders.Neat;
using SharpNeat.DistanceMetrics;
using SharpNeat.Domains.BinaryThreeMultiplexer;
using SharpNeat.EvolutionAlgorithms;
using SharpNeat.EvolutionAlgorithms.ComplexityRegulation;
using SharpNeat.Genomes.Neat;
using SharpNeat.Phenomes;
using SharpNeat.SpeciationStrategies;

namespace SharpNeat.Domains.ThreeTermBooleanIO
{
    class ThreeTermBooleanIOEvaluator : IPhenomeEvaluator<IBlackBox>
    {
        const double StopFitness = 100.0;
        ulong _evalCount;
        bool _stopConditionSatisfied;

        #region IPhenomeEvaluator<IBlackBox> Members

        /// <summary>
        /// Gets the total number of evaluations that have been performed.
        /// </summary>
        public ulong EvaluationCount
        {
            get { return _evalCount; }
        }

        /// <summary>
        /// Gets a value indicating whether some goal fitness has been achieved and that
        /// the evolutionary algorithm/search should stop. This property's value can remain false
        /// to allow the algorithm to run indefinitely.
        /// </summary>
        public bool StopConditionSatisfied
        {
            get { return _stopConditionSatisfied; }
        }

        /// <summary>
        /// The minimum magnitude between results for them to be marked as successful
        /// </summary>
        private double DELTA = 0.4;

        /// <summary>
        /// Evaluate the provided IBlackBox against the Binary 6-Multiplexer problem domain and return
        /// its fitness score.
        /// </summary>
        public FitnessInfo Evaluate(IBlackBox box)
        {
            double fitness = 0.0;
            bool success = true;
            double[] output = new double[3];
            double[] input = new double[3];

            ISignalArray inputArr = box.InputSignalArray;
            ISignalArray outputArr = box.OutputSignalArray;
            _evalCount++;

            var inputs = new List<double[]>
            {
                new[] {0.0, 0.0, 0.0},
                new[] {0.0, 0.0, 1.0},
                new[] {0.0, 1.0, 0.0},
                new[] {0.0, 1.0, 1.0},
                new[] {1.0, 0.0, 0.0},
                new[] {1.0, 0.0, 1.0},
                new[] {1.0, 1.0, 0.0},
                new[] {1.0, 1.0, 1.0}
            };

            var outputs = new List<double[]>
            {
                   //a==b, a!=c, a||b||C
                new[] {1.0, 0.0, 0.0},
                new[] {1.0, 1.0, 1.0},
                new[] {0.0, 0.0, 1.0},
                new[] {0.0, 1.0, 1.0},
                new[] {0.0, 1.0, 1.0},
                new[] {0.0, 0.0, 1.0},
                new[] {1.0, 1.0, 1.0},
                new[] {1.0, 0.0, 1.0}
            };

            // 3 test cases.
            for (int i = 0; i < inputs.Count; i++)
            {
                //initialise the inputs
                for (int j = 0; j < 3; j++)
                {
                    inputArr[j] = inputs[i][j];
                }


                // Activate the black box.
                box.Activate();
                if (!box.IsStateValid)
                {
                    // Any black box that gets itself into an invalid state is unlikely to be
                    // any good, so let's just exit here.
                    return FitnessInfo.Zero;
                }

                // Read output signal.
                for (int j = 0; j < 3; j++)
                {
                    output[j] = outputArr[j];
                }

                Debug.Assert(output.Sum() >= 0.0, "Unexpected negative output.");

                var targets = outputs[i];


                for (int j = 0; j < targets.Length; j++)
                {
                    if (Math.Abs(targets[j] - output[j]) <= DELTA)
                    {
                        //This was a success, so give top marks and continue
                        fitness++;
                        continue;
                    }

                    // mark it as a failure if the magnitude of differences between any target and actual output is greater than a given delta
                    success = false;
                    if (targets[j] == 1.0)
                    {
                        fitness += 1.0 - ((1.0 - output[j]) * (1.0 - output[j]));
                    }
                    else
                    {
                        //this works fine when the target output is 1, but with a goal of zero, the fitness always increments by a constant +1
                        fitness += 1.0 - (output[j] * output[j]);
                    }
                }


                // Reset black box state ready for next test case.
                box.ResetState();
            }

            // If the correct answer was given in each case then add a bonus value to the fitness.
            if (success)
            {
                fitness += 100.0;
            }

            if (fitness >= StopFitness)
            {
                _stopConditionSatisfied = true;
            }

            return new FitnessInfo(fitness, fitness);
        }

        /// <summary>
        /// Reset the internal state of the evaluation scheme if any exists.
        /// Note. The Binary Multiplexer problem domain has no internal state. This method does nothing.
        /// </summary>
        public void Reset()
        {
        }

        #endregion
    }
}