from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import numpy as np
import pandas as pd
from flask_cors import CORS, cross_origin
import pickle

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

encoder = pickle.load(open('../Model/encoder.pkl', 'rb'))
final_model = pickle.load(open('../Model/final_model.pkl', 'rb'))
kmeans_1 = pickle.load(open('../Model/kmeans_1.pkl', 'rb'))
kmeans_2 = pickle.load(open('../Model/kmeans_2.pkl', 'rb'))
scaler = pickle.load(open('../Model/scaler.pkl', 'rb'))

formValues = reqparse.RequestParser()
formValues.add_argument("no_of_adults", type=int, help="Number of adults required", required=True)
formValues.add_argument("no_of_children", type=int, help="Number of children required", required=True)
formValues.add_argument("no_of_weekend_nights", type=int, help="Number of weekend nights", required=True)
formValues.add_argument("no_of_week_nights", type=int, help="Number of week nights", required=True)
formValues.add_argument("booking_date", type=str, help="Booking date required", required=True)
formValues.add_argument("arrival_date", type=str, help="Arrival date required", required=True)
formValues.add_argument("no_of_previous_cancellations", help="Number of previous cancellations required", type=int, required=True)
formValues.add_argument("no_of_previous_bookings_not_canceled", help="Number of previous bookings not canceled", type=int, required=True)
formValues.add_argument("avg_price_per_room", type=int, help="Average price of each room required", required=True)
formValues.add_argument("no_of_special_requests", type=int, help="Number of special requests required", required=True)
formValues.add_argument("type_of_meal_plan", type=int, help="Types of meal plan required", required=True)
formValues.add_argument("required_car_parking_space", type=int, help="Required car parking space required", required=True)
formValues.add_argument("room_type_reserved", type=int, help="Reserved room type required", required=True)
formValues.add_argument("repeated_guest", type=bool, help="Repeated guest required", required=True)
formValues.add_argument("market_segment_type", type=int, help="Market segment type required", required=True)

class Prediction(Resource):
    def get(self):
        return {"name" : "Lewis Hamilton"}
    def post(self):
        argument = formValues.parse_args()
        
        no_of_adults = argument['no_of_adults']
        no_of_children = argument['no_of_children']
        no_of_weekend_nights = argument['no_of_weekend_nights']
        no_of_week_nights = argument['no_of_week_nights']
        type_of_meal_plan = argument['type_of_meal_plan']
        required_car_parking_space = argument['required_car_parking_space']
        room_type_reserved = argument['room_type_reserved']
        lead_time = (pd.to_datetime(argument['arrival_date']).dayofyear - pd.to_datetime(argument['booking_date']).dayofyear)
        arrival_year = (pd.to_datetime(argument['arrival_date']).year)
        arrival_month = (pd.to_datetime(argument['arrival_date']).month)
        arrival_date = (pd.to_datetime(argument['arrival_date']).day)
        market_segment_type = argument['market_segment_type']
        repeated_guest = int(argument['repeated_guest'])
        no_of_previous_cancellations = argument['no_of_previous_cancellations']
        no_of_previous_bookings_not_canceled = argument['no_of_previous_bookings_not_canceled']
        avg_price_per_room = (argument['avg_price_per_room'])
        no_of_special_requests = argument['no_of_special_requests']

        # OneHot encoding for the categorical features
        categorical_feature = np.array([[type_of_meal_plan, required_car_parking_space, room_type_reserved, market_segment_type, repeated_guest]])
        categorical_feature = pd.DataFrame(categorical_feature, columns=['type_of_meal_plan', 'required_car_parking_space', 'room_type_reserved',
                                                                         'market_segment_type', 'repeated_guest'])
        encoded_categorical_features = encoder.transform(categorical_feature)
        encoded_categorical_features = list((encoded_categorical_features)[0])

        type_of_meal_plan_0 = encoded_categorical_features[0]
        type_of_meal_plan_1 = encoded_categorical_features[1]
        type_of_meal_plan_2 = encoded_categorical_features[2]
        type_of_meal_plan_3 = encoded_categorical_features[3]
        required_car_parking_space_0 = encoded_categorical_features[4]
        required_car_parking_space_1 = encoded_categorical_features[5]
        room_type_reserved_0 = encoded_categorical_features[6]
        room_type_reserved_1 = encoded_categorical_features[7]
        room_type_reserved_2 = encoded_categorical_features[8]
        room_type_reserved_3 = encoded_categorical_features[9]
        room_type_reserved_4 = encoded_categorical_features[10]
        room_type_reserved_5 = encoded_categorical_features[11]
        room_type_reserved_6 = encoded_categorical_features[12]
        market_segment_type_0 = encoded_categorical_features[13]
        market_segment_type_1 = encoded_categorical_features[14]
        market_segment_type_2 = encoded_categorical_features[15]
        market_segment_type_3 = encoded_categorical_features[16]
        market_segment_type_4 = encoded_categorical_features[17]
        repeated_guest_0 = encoded_categorical_features[18]
        repeated_guest_1 = encoded_categorical_features[19]

        # Creating new features
        total_no_of_members = no_of_adults + no_of_children
        total_no_of_nights = no_of_week_nights + no_of_weekend_nights
        no_of_adults_div_price = no_of_adults / (avg_price_per_room + 1e-6)
        no_of_children_div_price = no_of_children / (avg_price_per_room + 1e-6)

        # Creating new feature using kmeans
        k_means_features = [[lead_time, avg_price_per_room, no_of_adults_div_price, market_segment_type_1, market_segment_type_0, no_of_special_requests, 
                    arrival_month, repeated_guest_0, arrival_year, required_car_parking_space_0]]
        k_means_features = pd.DataFrame(k_means_features, 
                                        columns=['lead_time', 'avg_price_per_room', 'no_of_adults_div_price', 'market_segment_type_1', 'market_segment_type_0', 
                                        'no_of_special_requests', 'arrival_month', 'repeated_guest_0', 'arrival_year', 'required_car_parking_space_0'])
        cluster_6 = kmeans_1.predict(k_means_features)[0]
        cluster_7 = kmeans_2.predict(k_means_features)[0]

        ### Note: We are not using the categorical features in the prediction
        
        # Scaling all the numerical columns
        encoded_cols = ['type_of_meal_plan_0', 'type_of_meal_plan_1', 'type_of_meal_plan_2', 'type_of_meal_plan_3', 'required_car_parking_space_0', 
        'required_car_parking_space_1', 'room_type_reserved_0', 'room_type_reserved_1', 'room_type_reserved_2', 'room_type_reserved_3', 'room_type_reserved_4', 
        'room_type_reserved_5', 'room_type_reserved_6', 'market_segment_type_0', 'market_segment_type_1', 'market_segment_type_2', 'market_segment_type_3', 
        'market_segment_type_4', 'repeated_guest_0', 'repeated_guest_1']
        scaling_column = ['no_of_adults','no_of_children','no_of_weekend_nights','no_of_week_nights','lead_time','arrival_year','arrival_month','arrival_date',
                          'no_of_previous_cancellations','no_of_previous_bookings_not_canceled','avg_price_per_room','no_of_special_requests']+encoded_cols
        scaling_column = scaling_column + ['total_no_of_members','total_no_of_nights','no_of_adults_div_price','no_of_children_div_price']

        # Numerical features
        numerical_features = np.array([[no_of_adults, no_of_children, no_of_weekend_nights, no_of_week_nights, lead_time, arrival_year, arrival_month, 
                              arrival_date, no_of_previous_cancellations, no_of_previous_bookings_not_canceled, avg_price_per_room, no_of_special_requests,
                              type_of_meal_plan_0, type_of_meal_plan_1, type_of_meal_plan_2, type_of_meal_plan_3, required_car_parking_space_0,
                              required_car_parking_space_1, room_type_reserved_0, room_type_reserved_1, room_type_reserved_2, room_type_reserved_3,
                              room_type_reserved_4, room_type_reserved_5, room_type_reserved_6, market_segment_type_0, market_segment_type_1, 
                              market_segment_type_2,
                              market_segment_type_3, market_segment_type_4, repeated_guest_0, repeated_guest_1, total_no_of_members, total_no_of_nights,
                              no_of_adults_div_price, no_of_children_div_price]])
        
        numerical_feature_table = pd.DataFrame(numerical_features, columns=scaling_column)
        numerical_feature_table = scaler.transform(numerical_feature_table)

        # Adding the cluster_6 and cluster_7 features
        numerical_feature_table = numerical_feature_table[0].T
        numerical_feature_table = list(numerical_feature_table)
        numerical_feature_table.append(cluster_6)
        numerical_feature_table.append(cluster_7)
        numerical_feature_table = np.array(numerical_feature_table)
        numerical_feature_table = np.array([numerical_feature_table])
        
        prediction_proba = final_model.predict_proba(numerical_feature_table)[0][1].astype("float")
        prediction = final_model.predict(numerical_feature_table)[0].astype("float")

        return {"prediction_proba" : prediction_proba, "prediction": prediction}

api.add_resource(Prediction, '/prediction')
    
if __name__ == "__main__":
    app.run(debug=True)