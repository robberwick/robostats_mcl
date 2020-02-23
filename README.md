fork of sjobeek:master, adapted for Tauradigm, a piwars entry.


Parameters that need tunign to the hardware


in T_run_mcl
laser sensor parameters
*stdev_cm = 10
*uniform_weight = 0.2

robot_particle
*log_prob_descale
*sigma_fwd_pct=0.2
*sigma_theta_pct=0.02

ParticleMap parameters
*target_particles = 300
*draw_max=2000
*resample_period=3



in montecarlo_localisation
mcl_update
*if sum(particle_list_weights) < 0.01

robot_particle
T_update_measurement_likelihood
*sensor offsets
