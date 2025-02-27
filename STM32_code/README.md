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

![image](https://github.com/user-attachments/assets/0d5e1648-afb1-4523-ae3c-d374a8c33b2e)


Find plugin

![image](https://github.com/user-attachments/assets/5ff52040-84c2-4e14-8214-571457999bee)


Check if it setup properly

![image](https://github.com/user-attachments/assets/76c8f320-88b0-480e-8c4c-51a1b63aebf8)


### Setup X-CUBE-AI plugin
Add new model in plugin

![image](https://github.com/user-attachments/assets/346b564b-d487-4936-ad58-d5ef5b4044f9)


Add your own model

![image](https://github.com/user-attachments/assets/fa90a613-b15a-4a41-9786-d660bdc432e5)


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

