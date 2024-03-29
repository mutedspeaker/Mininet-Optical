The goal is to develop an Optical Spectrum as a Service (OSaaS) system that can predict how channels on a 
given bandwidth slot will behave based on data collected from other bands. The system aims to calculate the 
average and maximum expected error for different fiber loads and channel allocations.

To achieve this, the system will first examine how external channels impact the target band, and then analyze
how the target band influences external channels. The plan is to create a topology in mn-optical and analyze a
specific spectral window, treating the rest as separate entities. The system will also assess how signals in 
the window are affected by dynamically changing loads outside of it.

To devise a load analysis strategy, the system will compare starting with channels near the window and progressing 
outward, a random approach, and a mixed strategy. The system will also experiment with different amplifier profiles. 
The ultimate goal is to determine the best strategy for achieving accurate channel behavior prediction and may involve 
the use of machine learning as a learning tool.
