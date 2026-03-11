
# 🎱 Sinai Billiard: From Microscopic Chaos to Macroscopic Diffusion

This repository contains a from-scratch Python/Pygame simulation of a Sinai billiard system. The goal of this project is to model how a purely deterministic, chaotic microscopic dynamic gives rise to a stochastic, macroscopic diffusion process. 

This numerical experiment serves as a foundational study of stochastic processes, laying the physical intuition for understanding reverse-time diffusion in Score-Based Generative Models.

## 🎥 Visualizing Diffusion
https://github.com/user-attachments/assets/73812e46-cbf7-4746-bad0-372b54baae2c

*Red particles progressively diffuse outward through a lattice of vibrating obstacles (phonons), illustrating the dilution of information over time.*

## 🔬 Key Physics & Computational Features
* **Numerical Integration:** Implementation of integration methods (Euler/RK4) to solve the equations of motion.
* **Microscopic Chaos:** Estimation of the **Lyapunov exponent** ($\lambda$) to quantify the chaotic divergence of nearby trajectories due to obstacle collisions (similar to Brownian motion)
* **Macroscopic Validation:** Extraction of the **diffusion coefficient** via linear regression of the mean squared displacement ($\langle d^2 \rangle \propto t$).
* **Extended Physics:** Implementation of magnetic fields (Lorentz force) and dynamic obstacles (phonons) to study their impact on the diffusion regime. 



`Python` | `NumPy` (Linear Algebra) | `Pygame` (Engine & Visualization) | `Matplotlib` (Data Analysis)









