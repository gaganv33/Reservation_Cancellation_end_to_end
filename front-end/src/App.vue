<template>
  <nav>
    <h1 class="text-center">Reservation Cancellation Prediction</h1>
    <div class="container border border-2 col-6 offset-3" id="Form" v-if="!isPred">
      <form @submit.prevent="getPrediction">
        <label for="adults" class="form-label">Number of Adults</label>
        <input v-model="formData.no_of_adults" type="number" class="form-control" id="adults" placeholder="Total number of adults" min="0" required >
        <br>
        <label for="children" class="form-label">Number of Children</label>
        <input v-model="formData.no_of_children" type="number" class="form-control" id="children" placeholder="Total number of children" min="0" required >
        <br>
        <label for="week_nights" class="form-label">Number of Week Nights</label>
        <input v-model="formData.no_of_week_nights" type="number" class="form-control" id="week_nights" placeholder="Total number of Week Nights" min="0"         
          required >
        <br>
        <label for="weekend_nights" class="form-label">Number of Weekend Nights</label>
        <input v-model="formData.no_of_weekend_nights" type="number" class="form-control" id="weekend_nights" placeholder="Total number of Weekend Nights" 
          min="0" required >
        <br>
        <label for="booking_date" class="form-label">Booking Date</label>
        <input v-model="formData.booking_date" type="date" class="form-control" id="booking_date" required >
        <br>
        <label for="arrival_date" class="form-label">Arrival Date</label>
        <input v-model="formData.arrival_date" type="date" class="form-control" id="arrival_date" required >
        <br>
        <label for="no_of_previous_cancellations" class="form-label">Total number of previous cancellations</label>
        <input v-model="formData.no_of_previous_cancellations" type="number" class="form-control" id="no_of_previous_cancellations" placeholder="Total number of 
          previous cancellations" required >
        <br>
        <label for="no_of_previous_bookings_not_canceled" class="form-label">Total number of previous bookings not canceled</label>
        <input v-model="formData.no_of_previous_bookings_not_canceled" type="number" class="form-control" id="no_of_previous_bookings_not_canceled" 
          placeholder="Total number of previous bookings not canceled" min="0" required >
        <br>
        <label for="avg_price_per_room" class="form-label">Average price per room</label>
        <input v-model="formData.avg_price_per_room" type="number" class="form-control" id="avg_price_per_room" placeholder="Average price per room" required 
          min="0" step="0.001">
        <br>
        <label for="no_of_special_requests" class="form-label">Total number of special requests</label>
        <input v-model="formData.no_of_special_requests" type="number" class="form-control" id="no_of_special_requests" placeholder="Total number of special 
          requests" min="0" required >
        <br>
        <label for="type_of_meal_plan" class="form-label">Type of meal plan</label>
        <input v-model="formData.type_of_meal_plan" type="number" class="form-control" id="type_of_meal_plan" placeholder="Type of meal plan" min="0" max="3" 
          required >
        <br>
        <label for="required_car_parking_space" class="form-label">Required car parking space</label>
        <input v-model="formData.required_car_parking_space" type="number" class="form-control" id="required_car_parking_space" placeholder="Required car parking 
          space" min="0" max="1" required >
        <br>
        <label for="room_type_reserved" class="form-label">Room type reserved</label>
        <input v-model="formData.room_type_reserved" type="number" class="form-control" id="room_type_reserved" placeholder="Room type reserved" min="0" max="6" 
          required >
        <br>
        <label for="market_segment_type" class="form-label">Market segment type</label>
        <input v-model="formData.market_segment_type" type="number" class="form-control" id="market_segment_type" placeholder="Market segment type" min="0" 
          max="4" required >
        <br>
        <label class="form-label">Repeated guest</label>
        <br>
        <span>
          <input v-model="formData.repeated_guest" type="radio" name="check" value=true>True
          <input v-model="formData.repeated_guest" type="radio" name="check" value=false>False
        </span>
        <button class="btn btn-success">Submit</button>
      </form>
    </div>
    <div class="container border border-2 col-6 offset-3" id="Form" v-if="isPred">
      <h2 class="text-center">Predicted value: {{ prediction.prediction }}</h2>
      <h2 class="text-center">Cancellation Probability: {{ prediction.prediction_proba }}</h2>
      <button class="btn btn-danger" @click.prevent="displayForm">Close</button>
    </div>
  </nav>
  <router-view/>
</template>

<script>
import axios from 'axios';
export default {
  data(){
    return {
      formData : {
        'no_of_adults' : 0,
        'no_of_children' : 0,
        'no_of_weekend_nights' : 0,
        'no_of_week_nights' : 0,
        'booking_date' : "2017-01-01",
        'arrival_date' : "2017-01-02",
        'no_of_previous_cancellations': 0,
        'no_of_previous_bookings_not_canceled' : 0,
        'avg_price_per_room' : 0,
        'no_of_special_requests' : 0,
        'type_of_meal_plan' : 0,
        'required_car_parking_space' : 0,
        'room_type_reserved' : 0,
        'repeated_guest' : false,
        'market_segment_type': 0,
      },
      prediction : {},
      isPred : false,
    }
  },
  methods : {
    async getPrediction(){
      try{
        const response = await axios.post('http://127.0.0.1:5000/prediction', this.formData);
        this.prediction = response.data;
        this.isPred = true;
      }
      catch(err){
        console.log("err", err);
      }
    },
    displayForm(){
      this.isPred = false;
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
#Form{
  border-radius: 0.7rem;
  padding: 1rem;
}
@import'~bootstrap/dist/css/bootstrap.css'
</style>
