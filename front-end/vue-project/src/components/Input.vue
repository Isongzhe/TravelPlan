<!-- components/FormInput.vue -->
<script setup lang="ts">
import { ref , onMounted, watch } from 'vue'; // Add the missing import statement for the 'watch' function

import FlatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.min.css';
import type { BaseOptions } from 'flatpickr/dist/types/options';


const config: Partial<BaseOptions> = {
  minDate: "today",
  mode: 'range',
  dateFormat: 'Y-m-d',
};

interface Airport {
  code: string;
  name: string;
}

interface TravelTime {
  start: string;
  end: string;
}

interface InputForm {
  googleMapURL: string;
  dateRange: string;
  timeRange: TravelTime;
  departureAirport: Airport;
  returnAirport: Airport;
}

const form = ref<InputForm>({
  googleMapURL: '',
  dateRange: '',
  timeRange: { start: '', end: '' },
  departureAirport: { code: '', name: '' },
  returnAirport: { code: '', name: '' },
});
const formStatus = ref('');

const allAirports = [
  { code: 'TPE', name: '桃園機場' },
  { code: 'TSA', name: '松山機場' },
  // 其他機場
];

const submit = () => {
  if (!form.value.dateRange || form.value.googleMapURL === '') {
    formStatus.value = '請填寫所有欄位';
    return;
  }
    formStatus.value = '資料送出中...';
    console.log(form.value.dateRange);
    console.log(form.value.googleMapURL);
    // 這裡可以寫 fetch API 的程式碼
};
</script>

<template>
<div class="container">
  <div class="inputBlock">
    <div class="airportInput">
      <h3>請選擇抵達機場</h3>
      <input list="departureAirports" v-model="form.departureAirport.code" placeholder="請輸入或選擇機場...." />
      <datalist id="departureAirports">
        <option value="TPE">桃園機場</option>
        <option value="TSA">松山機場</option>
        <!-- 其他機場 -->
      </datalist>
    </div>

    <div class="airportInput">
      <h3>請選擇返回機場</h3>
      <input list="returnAirports" v-model="form.returnAirport.code" placeholder="請輸入或選擇機場...." />
      <datalist id="returnAirports">
        <option value="TPE">桃園機場</option>
        <option value="TSA">松山機場</option>
        <!-- 其他機場 -->
      </datalist>
    </div>
  
  </div>


  <div class="inputBlock">
    <div class="timeInput">
      <div class="daterange">
        <h3>請輸入旅遊抵達日期與離境日期</h3>
        <flat-pickr v-model="form.dateRange" :config="config" />
      </div>
      <div class="timerange">
        <h3>請輸入開始旅行的時間</h3>
        <input type="time" v-model="form.timeRange.start" />

        <h3>請輸入結束旅行的時間</h3>
        <tag>(建議:回程班機前3個小時)</tag>
        <input type="time" v-model="form.timeRange.end" />
      </div>
    </div>
  </div>

  <div>
      <h3>請輸入GoogleMap清單連結</h3>
      <input v-model="form.googleMapURL" placeholder="請輸入 Google Map URL...." />
  </div>

  <div>    
      <button @click="submit">提交</button>
      <p> {{ formStatus }} </p>
  </div>

</div>
  
</template>

<style>
@import 'flatpickr/dist/flatpickr.min.css';

body {
    font-family: 'Roboto', sans-serif;
    background-color: #f5f5f5;
    font-size: 18px; /* 設定全域字體大小 */
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px; /* 增大邊框半徑 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
    transition: box-shadow 0.3s ease; /* 增加陰影的過渡效果 */
}


.inputBlock {
  display: flex;
  align-items: center;
}

.inputBlock:last-child {
  margin-right: 0;
}
h3 {
    font-size: 20px; /* 增大字體大小 */
    margin-bottom: 10px;
}
input {
    display: block;
    width: 80%;
    padding: 10px;
    font-size: 12px; /* 增大字體大小 */
    margin-bottom: 10px;
    border: 1px solid #ccc; /* 增加邊框 */
    border-radius: 8px; /* 增大邊框半徑 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
    transition: box-shadow 0.3s ease, border-color 0.3s ease; /* 增加邊框顏色的過渡效果 */
}

input:focus {
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    border-color: #999; /* 當輸入框被選中時，變更邊框顏色 */
    outline: none; /* 移除預設的輪廓 */
}

div {
    margin-bottom: 10px;
}

button {
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
    background-color: #3f51b5;
    border: none;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

button:hover {
    background-color: #303f9f;
}

button:active {
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}
</style>