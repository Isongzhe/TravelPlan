<!-- components/FormInput.vue -->
<script setup lang="ts">
import { ref , onMounted } from 'vue';
import FlatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import type { BaseOptions } from 'flatpickr/dist/types/options';

const googleMapURL = ref('')
const dateRange = ref('');
const status = ref('');
const origin = ref('');
const destination = ref('');
const airports = ref([]);

const config: Partial<BaseOptions> = {
  minDate: "today",
  mode: 'range',
  dateFormat: 'Y-m-d',
};



const submit = () => {
  if (!dateRange.value || googleMapURL.value === '') {
    status.value = '請填寫所有欄位';
    return;
  }
    status.value = '資料送出中...';
    console.log(dateRange.value);
    console.log(googleMapURL.value);
    // 這裡可以寫 fetch API 的程式碼
};

</script>

<template>
    <div>
        <h3>請輸入旅遊起始地與目的地</h3>
        <select v-model="origin">
            <option v-for="airport in airports" :value="airport.code">{{ airport.name }}</option>
        </select>
        <select v-model="destination">
            <option v-for="airport in airports" :value="airport.code">{{ airport.name }}</option>
        </select>
    </div>   

    <div>
        <h3>請輸入旅遊抵達日期與離境日期</h3>
        <flat-pickr v-model="dateRange" :config="config" />
    </div>

    <div>
        <h3>請輸入GoogleMap清單連結</h3>
        <input v-model="googleMapURL" placeholder="請輸入 Google Map URL...." />
    </div>

    <div>    
        <button @click="submit">提交</button>
        <p> {{ status }} </p>
    </div>
</template>

<style>
@import 'flatpickr/dist/flatpickr.min.css';

body {
    font-family: 'Roboto', sans-serif;
    background-color: #f5f5f5;
}
input {
    display: block;
    width: 50%;
    padding: 10px;
    font-size: 18px;
    margin-bottom: 10px;
    border: none;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
    transition: box-shadow 0.3s ease;
}

input:focus {
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

div {
    margin-bottom: 20px;
}

button {
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
    background-color: #3f51b5;
    color: white;
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