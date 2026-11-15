You built `fill_features`, which fills missing features from a defaults dictionary before the model scores a delivery-time request. In production an upstream team renames a field, and for two days the `courier_distance_km` feature is missing from every request. Nothing crashes and the service returns scores.

An interviewer asks: "What should the system do when a feature is missing at serving time, and how would you have noticed this one sooner?" Explain your design choice and one risk of filling with defaults.
