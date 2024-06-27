<template>
  <div>
    <h2>Результаты поиска</h2>
    <div v-for="room in rooms" :key="room.id">
      <h3>{{ room.name }}</h3>
      <p>Тип: {{ room.room_type }}</p>
      <p>Цена: {{ room.price }}</p>
      <p>Вместимость: {{ room.capacity }}</p>
      <button @click="bookRoom(room)">Забронировать</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  data() {
    return {
      rooms: [],
      userId: '',
      checkIn: '',
      checkOut: ''
    };
  },
  created() {
    const roomsData = this.$route.query.rooms;
    if (roomsData) {
      this.rooms = JSON.parse(roomsData);
    }

    this.checkIn = this.$route.query.check_in || '';
    this.checkOut = this.$route.query.check_out || '';

    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.userId = decodedToken.sub;
    }
  },
  methods: {
    async bookRoom(room) {
  try {
    const checkIn = this.$route.query.check_in;
    const checkOut = this.$route.query.check_out;
    const totalNights = this.calculateNights(checkIn, checkOut);
    const totalPrice = room.price * totalNights;

    const bookingData = {
      room_id: room.id,
      user_id: this.userId.id,
      check_in: checkIn,
      check_out: checkOut,
      total_price: totalPrice
    };

    console.log('Booking data to be sent:', bookingData);

    await axios.post('http://localhost:5000/bookings', bookingData);

    this.$router.push('/');
  } catch (error) {
    console.error('Ошибка при бронировании номера:', error);
  }
},
    calculateNights(checkIn, checkOut) {
      const date1 = new Date(checkIn);
      const date2 = new Date(checkOut);
      const timeDifference = Math.abs(date2.getTime() - date1.getTime());
      const nightCount = Math.ceil(timeDifference / (1000 * 3600 * 24));
      return nightCount;
    }
  }
};
</script>

<style scoped>
.room-card {
  border: 1px solid #ccc;
  padding: 16px;
  margin: 8px 0;
}
</style>