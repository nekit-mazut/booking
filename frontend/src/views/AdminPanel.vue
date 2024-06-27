<template>
  <div>
    <h1>Admin Panel</h1>

    <section v-if="!isAuthenticated">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div>
          <label>Username:</label>
          <input type="text" v-model="loginForm.username" required>
        </div>
        <div>
          <label>Password:</label>
          <input type="password" v-model="loginForm.password" required>
        </div>
        <button type="submit">Login</button>
      </form>
    </section>

    <section v-if="isAuthenticated">
      <h2>Create User</h2>
      <form @submit.prevent="createUser">
        <div>
          <label>Username:</label>
          <input type="text" v-model="createUserForm.username" required>
        </div>
        <div>
          <label>Email:</label>
          <input type="email" v-model="createUserForm.email" required>
        </div>
        <div>
          <label>Password:</label>
          <input type="password" v-model="createUserForm.password" required>
        </div>
        <button type="submit">Create User</button>
      </form>
    </section>

    <section v-if="isAuthenticated">
      <h2>Update User</h2>
      <form @submit.prevent="updateUser">
        <div>
          <label>User ID:</label>
          <input type="number" v-model="updateUserForm.userId" required>
        </div>
        <div>
          <label>Username:</label>
          <input type="text" v-model="updateUserForm.username">
        </div>
        <div>
          <label>Email:</label>
          <input type="email" v-model="updateUserForm.email">
        </div>
        <div>
          <label>Password:</label>
          <input type="password" v-model="updateUserForm.password">
        </div>
        <button type="submit">Update User</button>
      </form>
    </section>

    <section v-if="isAuthenticated">
      <h2>Delete User</h2>
      <form @submit.prevent="deleteUser">
        <div>
          <label>User ID:</label>
          <input type="number" v-model="deleteUserId" required>
        </div>
        <button type="submit">Delete User</button>
      </form>
    </section>

    <section v-if="isAuthenticated">
      <h2>User Bookings</h2>
      <form @submit.prevent="getUserBookings">
        <div>
          <label>User ID:</label>
          <input type="number" v-model="bookingsUserId" required>
        </div>
        <button type="submit">Get Bookings</button>
      </form>
      <div v-if="bookings.length">
        <h3>Bookings:</h3>
        <ul>
          <li v-for="booking in bookings" :key="booking.id">
            <p>Booking ID: {{ booking.id }}</p>
            <p>Booking Date: {{ booking.date }}</p>
            <p>Booking Status: {{ booking.status }}</p>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>см. в консоль</p>
      </div>
    </section>

    <section v-if="isAuthenticated">
      <h2>Create Room</h2>
      <form @submit.prevent="createRoom">
        <div>
          <label>Name:</label>
          <input type="text" v-model="createRoomForm.name" required>
        </div>
        <div>
          <label>Room Type:</label>
          <input type="text" v-model="createRoomForm.roomType" required>
        </div>
        <div>
          <label>Price:</label>
          <input type="number" v-model="createRoomForm.price" required>
        </div>
        <div>
          <label>Capacity:</label>
          <input type="number" v-model="createRoomForm.capacity" required>
        </div>
        <button type="submit">Create Room</button>
      </form>
    </section>

    <section v-if="isAuthenticated">
      <h2>Update Room</h2>
      <form @submit.prevent="updateRoom">
        <div>
          <label>Room ID:</label>
          <input type="number" v-model="updateRoomForm.roomId" required>
        </div>
        <div>
          <label>Name:</label>
          <input type="text" v-model="updateRoomForm.name">
        </div>
        <div>
          <label>Room Type:</label>
          <input type="text" v-model="updateRoomForm.roomType">
        </div>
        <div>
          <label>Price:</label>
          <input type="number" v-model="updateRoomForm.price">
        </div>
        <div>
          <label>Capacity:</label>
          <input type="number" v-model="updateRoomForm.capacity">
        </div>
        <button type="submit">Update Room</button>
      </form>
    </section>

    <section v-if="isAuthenticated">
      <h2>Cancel Booking</h2>
      <form @submit.prevent="cancelBooking">
        <div>
          <label>Booking ID:</label>
          <input type="number" v-model="cancelBookingForm.bookingId" required>
        </div>
        <button type="submit">Cancel Booking</button>
      </form>
    </section>

    <section v-if="isAuthenticated">
      <h2>Create Admin User</h2>
      <form @submit.prevent="createAdmin">
        <div>
          <label>Username:</label>
          <input type="text" v-model="createAdminForm.username" required>
        </div>
        <div>
          <label>Email:</label>
          <input type="email" v-model="createAdminForm.email" required>
        </div>
        <div>
          <label>Password:</label>
          <input type="password" v-model="createAdminForm.password" required>
        </div>
        <button type="submit">Create Admin</button>
      </form>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      createRoomForm: {
        name: '',
        roomType: '',
        price: null,
        capacity: null
      },
      updateRoomForm: {
        roomId: null,
        name: '',
        roomType: '',
        price: null,
        capacity: null
      },
      cancelBookingForm: {
        bookingId: null
      },
      isAuthenticated: false,
      createUserForm: {
        username: '',
        email: '',
        password: ''
      },
      updateUserForm: {
        userId: null,
        username: '',
        email: '',
        password: ''
      },
      deleteUserId: null,
      bookingsUserId: null,
      bookings: [],
      createAdminForm: {
        username: '',
        email: '',
        password: ''
      }
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:5001/login', this.loginForm);
        const token = response.data.access_token;
        localStorage.setItem('token', token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        this.isAuthenticated = true;
        this.resetForm('loginForm');
      } catch (error) {
        console.error('Error logging in:', error);
      }
    },
    async createUser() {
      try {
        const response = await axios.post('http://localhost:5001/users', this.createUserForm);
        console.log('User created successfully:', response.data);
        this.resetForm('createUserForm');
      } catch (error) {
        console.error('Error creating user:', error);
      }
    },
    async createRoom() {
      try {
        const response = await axios.post('http://localhost:5000/rooms', this.createRoomForm);
        console.log('Room created successfully:', response.data);
        this.resetForm('createRoomForm');
      } catch (error) {
        console.error('Error creating room:', error);
      }
    },
    async updateRoom() {
      try {
        const response = await axios.put(`http://localhost:5000/rooms/${this.updateRoomForm.roomId}`, {
          name: this.updateRoomForm.name,
          room_type: this.updateRoomForm.roomType,
          price: this.updateRoomForm.price,
          capacity: this.updateRoomForm.capacity
        });
        console.log('Room updated successfully:', response.data);
        this.resetForm('updateRoomForm');
      } catch (error) {
        console.error('Error updating room:', error);
      }
    },
    async cancelBooking() {
      try {
        const response = await axios.delete(`http://localhost:5000/bookings/${this.cancelBookingForm.bookingId}`);
        console.log('Booking cancelled successfully:', response.data);
        this.resetForm('cancelBookingForm');
      } catch (error) {
        console.error('Error cancelling booking:', error);
      }
    },
    async updateUser() {
      try {
        const response = await axios.put(`http://localhost:5001/users/${this.updateUserForm.userId}`, {
          username: this.updateUserForm.username,
          email: this.updateUserForm.email,
          password: this.updateUserForm.password
        });
        console.log('User updated successfully:', response.data);
        this.resetForm('updateUserForm');
      } catch (error) {
        console.error('Error updating user:', error);
      }
    },
    async deleteUser() {
      try {
        const response = await axios.delete(`http://localhost:5001/users/${this.deleteUserId}`);
        console.log('User deleted successfully:', response.data);
        this.deleteUserId = null;
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    async getUserBookings() {
      try {
        const response = await axios.get(`http://localhost:5001/users/${this.bookingsUserId}/bookings`);
        this.bookings = response.data;
        console.log('User bookings fetched successfully:', response.data);
        this.bookingsUserId = null;
      } catch (error) {
        console.error('Error fetching user bookings:', error);
      }
    },
    async createAdmin() {
      try {
        const response = await axios.post('http://localhost:5001/users/admin', this.createAdminForm);
        console.log('Admin created successfully:', response.data);
        this.resetForm('createAdminForm');
      } catch (error) {
        console.error('Error creating admin:', error);
      }
    },
    resetForm(formName) {
      this[formName] = {};
    }
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      this.isAuthenticated = true;
    }
  }
};
</script>

<style scoped>
section {
  margin-bottom: 40px;
}

form div {
  margin-bottom: 10px;
}

form label {
  display: block;
  margin-bottom: 5px;
}

form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  box-sizing: border-box;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>