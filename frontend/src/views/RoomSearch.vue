<template>
  <div class="room-search">
    <h1>Поиск номеров</h1>
    <form @submit.prevent="searchRooms">
      <div>
        <label>Тип комнаты:</label>
        <div v-for="type in roomTypes" :key="type">
          <input type="checkbox" :value="type" v-model="selectedRoomTypes">{{ type }}
        </div>
      </div>
      <div>
        <label>Цена от:</label>
        <input type="number" v-model="priceMin" />
      </div>
      <div>
        <label>Цена до:</label>
        <input type="number" v-model="priceMax" />
      </div>
      <div>
        <label>Вместимость:</label>
        <input type="number" v-model="capacity" />
      </div>
      <div>
        <label>Дата заезда:</label>
        <input type="date" v-model="checkIn" />
      </div>
      <div>
        <label>Дата выезда:</label>
        <input type="date" v-model="checkOut" />
      </div>
      <button type="submit">Поиск</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      roomTypes: [],
      selectedRoomTypes: [],
      priceMin: null,
      priceMax: null,
      capacity: null,
      checkIn: '',
      checkOut: ''
    };
  },
  created() {
    this.fetchRoomTypes();
  },
  methods: {
    async fetchRoomTypes() {
      try {
        const response = await axios.get('http://localhost:5000/room_types');
        this.roomTypes = response.data.room_types;
      } catch (error) {
        console.error('Ошибка при получении типов комнат:', error);
      }
    },
    async searchRooms() {
  try {
    const response = await axios.post('http://localhost:5000/rooms/search', {
      check_in: this.checkIn,
      check_out: this.checkOut,
      capacity: this.capacity,
      room_types: this.selectedRoomTypes,
      price_min: this.priceMin,
      price_max: this.priceMax
    });
    this.$router.push({
      path: '/results',
      query: {
        rooms: JSON.stringify(response.data.rooms),
        check_in: this.checkIn,  // Передаем check_in в query параметры
        check_out: this.checkOut  // Передаем check_out в query параметры
      }
    });
  } catch (error) {
    console.error('Ошибка при поиске комнат:', error);
  }
}
  }
};
</script>

<style scoped>
.room-search {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.room-search h1 {
  text-align: center;
  margin-bottom: 20px;
}

.room-search form {
  display: grid;
  gap: 10px;
}

.room-search label {
  font-weight: bold;
}

.room-search input[type="checkbox"],
.room-search input[type="number"],
.room-search input[type="date"] {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.room-search button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.room-search button:hover {
  background-color: #0056b3;
}
</style>