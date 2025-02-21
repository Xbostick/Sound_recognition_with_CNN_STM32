# STM32 CNN Deployment - C++ Source Code

## Overview
This README provides instructions on how to integrate and run the deployed **CNN model on STM32** using **X-CUBE-AI**. The focus is on modifying the relevant C source files and ensuring correct execution.

## 📂 Key Source Files
- **`./STM32_code/X-CUBE-AI/App/app_x-cube-ai.c`**  
  _(Handles AI model usage on the STM32)_ Look carefull there if you has problems with deploing or operating model. There is my implementation
- **`./STM32_code/Core/Src/main.c`**  
  _(Initializes the microcontroller and calls AI inference functions)_ There is minimal functional to operate STM32U5 with INMP441

## 🔷 ** Setting Up X-CUBE-AI**
### Install X-CUBE-AI plugin
Go to *Software packs *
screen1
Find plugin
screen2
Check if it setup properly
screen3
### Setup X-CUBE-AI plugin
Add new model in plugin
screen4
Add your own model
screen5
### 🔷 ** Editing sources files**
#### 📂 Key Source Files
- **`./STM32_code/X-CUBE-AI/App/app_x-cube-ai.c`**  
  _(Handles AI model usage on the STM32)_ Look carefull there if you has problems with deploing or operating model. There is my implementation
- **`./STM32_code/Core/Src/main.c`**  
  _(Initializes the microcontroller and calls AI inference functions)_ There is minimal functional to operate STM32U5 with INMP441


## 📝 Notes
- Ensure the model is converted to **TFLite format** and properly integrated.
- Debug using **serial output (UART)** to verify inference results.
- Check memory constraints and optimize for STM32 limitations.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🔹 **Contributions:** Feel free to open an issue or pull request!

