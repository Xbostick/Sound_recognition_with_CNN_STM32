
/**
  ******************************************************************************
  * @file    app_x-cube-ai.c
  * @author  X-CUBE-AI C code generator
  * @brief   AI program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */

 /*
  * Description
  *   v1.0 - Minimum template to show how to use the Embedded Client API
  *          model. Only one input and one output is supported. All
  *          memory resources are allocated statically (AI_NETWORK_XX, defines
  *          are used).
  *          Re-target of the printf function is out-of-scope.
  *   v2.0 - add multiple IO and/or multiple heap support
  *
  *   For more information, see the embeded documentation:
  *
  *       [1] %X_CUBE_AI_DIR%/Documentation/index.html
  *
  *   X_CUBE_AI_DIR indicates the location where the X-CUBE-AI pack is installed
  *   typical : C:\Users\<user_name>\STM32Cube\Repository\STMicroelectronics\X-CUBE-AI\7.1.0
  */

#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/

#if defined ( __ICCARM__ )
#elif defined ( __CC_ARM ) || ( __GNUC__ )
#endif

/* System headers */
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "app_x-cube-ai.h"
#include "main.h"
#include "ai_datatypes_defines.h"
#include "network.h"
#include "network_data.h"

/* USER CODE BEGIN includes */
#include "PreCulcMFCC.h"
#include <math.h>
#include "arm_math.h"

#define AUDIO_BUFF_SIZE FFTNum * FFTSize
#define FEATURES_BUFF_SIZE NNFeaturesNum
extern uint32_t pAudBuf[AUDIO_BUFF_SIZE];
extern UART_HandleTypeDef huart1;
static uint32_t pAudBufCopy[AUDIO_BUFF_SIZE] = {0}; 
float pFeatureBuf[FEATURES_BUFF_SIZE]; // Buff to storage preprocessed data. Raw inputs for NN
arm_mfcc_instance_f32 mfccf32;
float NN_output[4] =  {0,0,0,0};	
uint8_t is_last = 0;	
uint8_t LED_STATE = 0;
uint8_t is_silence = 0;
uint32_t timer = 0;
uint32_t sensivity = 2;
/* USER CODE END includes */

/* IO buffers ----------------------------------------------------------------*/

#if !defined(AI_NETWORK_INPUTS_IN_ACTIVATIONS)
AI_ALIGNED(4) ai_i8 data_in_1[AI_NETWORK_IN_1_SIZE_BYTES];
ai_i8* data_ins[AI_NETWORK_IN_NUM] = {
data_in_1
};
#else
ai_i8* data_ins[AI_NETWORK_IN_NUM] = {
NULL
};
#endif

#if !defined(AI_NETWORK_OUTPUTS_IN_ACTIVATIONS)
AI_ALIGNED(4) ai_i8 data_out_1[AI_NETWORK_OUT_1_SIZE_BYTES];
ai_i8* data_outs[AI_NETWORK_OUT_NUM] = {
data_out_1
};
#else
ai_i8* data_outs[AI_NETWORK_OUT_NUM] = {
NULL
};
#endif

/* Activations buffers -------------------------------------------------------*/

AI_ALIGNED(32)
static uint8_t pool0[AI_NETWORK_DATA_ACTIVATION_1_SIZE];

ai_handle data_activations0[] = {pool0};

/* AI objects ----------------------------------------------------------------*/

static ai_handle network = AI_HANDLE_NULL;

static ai_buffer* ai_input;
static ai_buffer* ai_output;

static void ai_log_err(const ai_error err, const char *fct)
{
  /* USER CODE BEGIN log */
  if (fct)
    printf("TEMPLATE - Error (%s) - type=0x%02x code=0x%02x\r\n", fct,
        err.type, err.code);
  else
    printf("TEMPLATE - Error - type=0x%02x code=0x%02x\r\n", err.type, err.code);

  do {} while (1);
  /* USER CODE END log */
}

static int ai_boostrap(ai_handle *act_addr)
{
  ai_error err;

  /* Create and initialize an instance of the model */
  err = ai_network_create_and_init(&network, act_addr, NULL);
  if (err.type != AI_ERROR_NONE) {
    ai_log_err(err, "ai_network_create_and_init");
    return -1;
  }

  ai_input = ai_network_inputs_get(network, NULL);
  ai_output = ai_network_outputs_get(network, NULL);

#if defined(AI_NETWORK_INPUTS_IN_ACTIVATIONS)
  /*  In the case where "--allocate-inputs" option is used, memory buffer can be
   *  used from the activations buffer. This is not mandatory.
   */
  for (int idx=0; idx < AI_NETWORK_IN_NUM; idx++) {
	data_ins[idx] = ai_input[idx].data;
  }
#else
  for (int idx=0; idx < AI_NETWORK_IN_NUM; idx++) {
	  ai_input[idx].data = data_ins[idx];
  }
#endif

#if defined(AI_NETWORK_OUTPUTS_IN_ACTIVATIONS)
  /*  In the case where "--allocate-outputs" option is used, memory buffer can be
   *  used from the activations buffer. This is no mandatory.
   */
  for (int idx=0; idx < AI_NETWORK_OUT_NUM; idx++) {
	data_outs[idx] = ai_output[idx].data;
  }
#else
  for (int idx=0; idx < AI_NETWORK_OUT_NUM; idx++) {
	ai_output[idx].data = data_outs[idx];
  }
#endif

  return 0;
}

static int ai_run(void)
{
  ai_i32 batch;

  batch = ai_network_run(network, ai_input, ai_output);
  if (batch != 1) {
    ai_log_err(ai_network_get_error(network),
        "ai_network_run");
    return -1;
  }

  return 0;
}

/* USER CODE BEGIN 2 */
void audio_preproc(float32_t* Src){
	 
	 float del = 268435456.0 / sensivity;
	 uint32_t temp;
	 float max_ampl = 0;
	 for (int i = 0; i < AUDIO_BUFF_SIZE; i++ ){
		temp = pAudBufCopy[i]; 
		Src[i] = ((int)temp<<8) / del ; 
		if (max_ampl < Src[i])
			max_ampl = Src[i];
	 }
	 
	 if (max_ampl <= 0.1)
		 is_silence = 1;
	 else
		 is_silence = 0;
	 
  

}


void compute_mfcc_CMSIS(arm_mfcc_instance_f32* mfccf32){
	float32_t temp[FFTSize*2];
	float32_t PreprocessedSound[AUDIO_BUFF_SIZE];
	float32_t PreprocessedSound_temp[FFTSize];
	//for (int i = 0 ; i < FFTNum; i ++)
		//HAL_UART_Transmit(&huart1,(uint8_t*)pAudBufCopy + i*4*FFTSize,sizeof(uint32_t)*FFTSize,100);
	audio_preproc(PreprocessedSound);
//	for (int i = 0 ; i < FFTNum; i ++)
//		HAL_UART_Transmit(&huart1,(uint8_t*)PreprocessedSound + i*4*FFTSize,sizeof(float)*FFTSize,100);
/*	//	Testing
	for(int i = 0; i < FFTSize; i ++)
		PreprocessedSound_temp[i] = test_mfcc[i];
	arm_mfcc_f32(&mfccf32, PreprocessedSound_temp,  pFeatureBuf, temp);
*/
	for(int i = 0; i < FFTNum; i ++){
		memcpy(PreprocessedSound_temp, PreprocessedSound + i * FFTSize, FFTSize * sizeof(float32_t));
		arm_mfcc_f32(mfccf32, PreprocessedSound_temp,  pFeatureBuf + i * numOfDctOutputs, temp);
	}
	//HAL_UART_Transmit(&huart1,(uint8_t*)pFeatureBuf,sizeof(float)*FEATURES_BUFF_SIZE,100);

}



int real = 0;


int acquire_and_process_data(ai_i8* data[])
{
		
	memcpy(pAudBufCopy, pAudBuf,AUDIO_BUFF_SIZE * sizeof(uint32_t));
	compute_mfcc_CMSIS(&mfccf32);
	ai_input[0].data = AI_HANDLE_PTR(pFeatureBuf);
	ai_output[0].data = AI_HANDLE_PTR(NN_output); 
  /* fill the inputs of the c-model
  for (int idx=0; idx < AI_NETWORK_IN_NUM; idx++ )
  {
      data[idx] = ....
  }

  */
  return 0;
}

int post_process(ai_i8* data[])
{
	/* amplitude > 0.1 and NN detected sound with conf >= 30%*/
	if (( NN_output[0] >= 0.3 || NN_output[1] >= 0.3 || NN_output[2] >= 0.3 || NN_output[3] >= 0.3) && is_silence==0 && LED_STATE==0){	
		uint8_t message_1[20] = "\nSound detecting";
		uint8_t message_2[20] = "\nModel confidence = ";
		uint8_t conf1 = floor(NN_output[0]*10);
    uint8_t conf2 = floor(NN_output[1]*10);
    uint8_t conf3 = floor(NN_output[2]*10);
		uint8_t conf4 = floor(NN_output[3]*10);
		LED_STATE = 1;
		timer = HAL_GetTick();
		HAL_GPIO_WritePin(LED_RED_GPIO_Port,LED_RED_Pin,0);
		HAL_UART_Transmit(&huart1,  message_1,17,10);
		HAL_UART_Transmit(&huart1, message_2,18,10);
		HAL_UART_Transmit(&huart1, &conf1,1,10);
		HAL_UART_Transmit(&huart1, &conf2,1,10);
    HAL_UART_Transmit(&huart1, &conf3,1,10);
		HAL_UART_Transmit(&huart1, &conf4,1,10);
		
	}
	/* amplitude < 0.1 and uart has been silenced 5000ms */
	if (is_silence && (HAL_GetTick() - timer > 5000)){
		timer = HAL_GetTick();
		uint8_t message_1[350] = "\nToo low ambient noise level";
		HAL_UART_Transmit(&huart1, message_1,31,10);
	}
	/* Power off LED if it has been powered 1000ms*/
	if ((HAL_GetTick() - timer > 1000) && LED_STATE ){
		timer = HAL_GetTick();
		HAL_GPIO_WritePin(LED_RED_GPIO_Port,LED_RED_Pin,1);
		LED_STATE = 0;
	}
		
	
		
  /* process the predictions
  for (int idx=0; idx < AI_NETWORK_OUT_NUM; idx++ )
  {
      data[idx] = ....
  }

  */
  return 0;
}
/* USER CODE END 2 */

/* Entry points --------------------------------------------------------------*/

void MX_X_CUBE_AI_Init(void)
{
    /* USER CODE BEGIN 5 */
  printf("\r\nTEMPLATE - initialization\r\n");
	arm_status status=arm_mfcc_init_f32(&mfccf32,FFTSize,numOfMelFilters,numOfDctOutputs,dctMatrixFilters,
        filtPos,filtLen,packedFilters,window);
  ai_boostrap(data_activations0);
	for(int i = 0 ; i < 10; i++){
	HAL_GPIO_WritePin(LED_RED_GPIO_Port,LED_RED_Pin,LED_STATE++%2);
	HAL_Delay(200);
	}
    /* USER CODE END 5 */
}

void MX_X_CUBE_AI_Process(void)
{
    /* USER CODE BEGIN 6 */
  int res = -1;
	
	

  printf("TEMPLATE - run - main loop\r\n");

  if (network) {

    do {
      /* 1 - acquire and pre-process input data */
      res = acquire_and_process_data(data_ins);
      /* 2 - process the data - call inference engine */
      if (res == 0)
        res = ai_run();
      /* 3- post-process the predictions */
      if (res == 0)
        res = post_process(data_outs);
    } while (res==0);
  }

  if (res) {
    ai_error err = {AI_ERROR_INVALID_STATE, AI_ERROR_CODE_NETWORK};
    ai_log_err(err, "Process has FAILED");
  }
    /* USER CODE END 6 */
}
#ifdef __cplusplus
}
#endif
