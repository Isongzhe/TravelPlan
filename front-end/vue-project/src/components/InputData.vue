<script setup lang="ts">

const inputValue = ref('')
import { ref, defineProps } from 'vue';

interface TravelPlaceInterface {
    original_name: string;
    name: string;
    address: string;
    location: {
        lat: number;
        lng: number;
    };
    types: string[];
}
let sampleData = [{
        "original_name": "今戶神社",
        "name": "Imado Shrine",
        "address": "1 Chome-5-22 Imado, Taito City, Tokyo 111-0024, Japan",
        "location": {
            "lat": 35.719319,
            "lng": 139.8035788
        },
        "types": [
            "tourist_attraction",
            "place_of_worship",
            "point_of_interest",
            "establishment"
        ]
    },
    {
        "original_name": "PARK STORE(cafe The SUN LIVES HERE)",
        "name": "PARK STORE(cafe The SUN LIVES HERE)",
        "address": "1 Chome-7-2 Ikejiri, Setagaya City, Tokyo 154-0001, Japan",
        "location": {
            "lat": 35.6420672,
            "lng": 139.6811874
        },
        "types": [
            "bakery",
            "point_of_interest",
            "store",
            "food",
            "establishment"
        ]
    },
    "Unatoto Unagi 的評論數 31 與期望的評論數 3693 不符。",
    {
        "original_name": "澀谷PARCO",
        "name": "Shibuya Parco",
        "address": "15-1 Udagawacho, Shibuya City, Tokyo 150-8377, Japan",
        "location": {
            "lat": 35.6620484,
            "lng": 139.6987767
        },
        "types": [
            "shopping_mall",
            "point_of_interest",
            "establishment"
        ]
    }
]

const travelPlace = ref<TravelPlaceInterface[] | null>(null);

// const submitURL = async () => {
//     const response = await fetch(`http://localhost:8000/api/scrape?url=${inputValue.value}`);
//     const data = await response.json();
//     console.log(data);
//     travelPlace.value = data
//         .filter((item: TravelPlaceInterface | string) => typeof item !== 'string')
//         .map((item: TravelPlaceInterface) => new TravelPlace(item));
// };
const submitURL = async () => {
    // 使用模擬數據，而不是從後端 API 獲取數據
    const data = sampleData;
    console.log(data);
    travelPlace.value = data
        .filter((item: TravelPlaceInterface | string) => typeof item !== 'string')
        .map((item => new TravelPlace(item));
};


class TravelPlace {
    original_name: string;
    name: string;
    address: string;
    location: {
        lat: number;
        lng: number;
    };
    types: string[];

    constructor(data: TravelPlaceInterface) {
        this.original_name = data.original_name;
        this.name = data.name;
        this.address = data.address;
        this.location = data.location;
        this.types = data.types;
    }

    getFullName() {
        return `${this.original_name} (${this.name})`;
    }

    getAddress() {
        return this.address;
    }

    getLocation() {
        return this.location;
    }

    getTypes() {
        return this.types.join(', ');
    }
}

</script>

<template>
    <div>
        <input v-model="inputValue" placeholder="請輸入...." />
        <button @click="submitURL">提交</button>
    </div>
    <div v-if="travelPlace===null"></div>
    <div v-else>
        <textarea name="" id="" cols="30" rows="10" v-text="JSON.stringify(travelPlace, null, 2)"></textarea>
        
        <div v-for="place in travelPlace" :key="place.name">
        <p>{{ place.getFullName() }}</p>
        <p v-if="place.location">緯度: {{ place.getLocation().lat }}</p>
        <p v-if="place.location">經度: {{ place.getLocation().lng }}</p>
        <p v-if="place.address">地址: {{ place.getAddress() }}</p>
        <p v-if="place.types">類型: {{ place.getTypes() }}</p>
        <p>----------------</p>

        </div>
    </div>
  

</template>

<style scoped>
div {
    margin-bottom: 20px;
}

input {
    display: block;
    width: 50%;
    padding: 10px;
    font-size: 16px;
    margin-bottom: 10px;
}

button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}

textarea {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    margin-bottom: 20px;
    resize: none;
}

h2 {
    font-size: 20px;
    margin-bottom: 10px;
}

p {
    font-size: 16px;
    margin-bottom: 10px;
}
</style>