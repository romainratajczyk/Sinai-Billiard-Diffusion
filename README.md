
# 🎱 Sinai Billiard: From Microscopic Chaos to Macroscopic Diffusion

This repository contains a from-scratch Python/Pygame simulation of a Sinai billiard system. The goal of this project is to model how a purely deterministic, chaotic microscopic dynamic gives rise to a stochastic, macroscopic diffusion process. 

This numerical experiment serves as a preliminary study of stochastic processes, laying the physical foundations necessary for understanding reverse-time diffusion generative models.

## 🎥 Visualizing Diffusion
https://github.com/user-attachments/assets/73812e46-cbf7-4746-bad0-372b54baae2c

*Red particles progressively diffuse outward through a lattice of vibrating obstacles (phonons), illustrating the dilution of information over time.*

## 🔬 Physics & Computational Features
* Implementation of integration methods (Euler/RK4) to solve the equations of motion.
* Estimation of the **Lyapunov exponent** ($\lambda$) to quantify the chaotic divergence of nearby trajectories due to obstacle collisions (similarly to Brownian motion)
* Extraction of the **diffusion coefficient** via linear regression of the mean squared displacement ($\langle D^2 \rangle \propto t$).
* Implementation of magnetic fields (Lorentz force) and dynamic obstacles (phonons) to study their impact on the diffusion regime. 



`Python` | `NumPy` (Linear Algebra) | `Pygame` (Engine & Visualization) | `Matplotlib` (Data Analysis)









