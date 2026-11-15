You built `drift_alarm`, which compares the mean and the spread of a live window of a feature with a reference window from training. The model estimates delivery time, and true delivery times arrive only a day later, so accuracy cannot be measured live.

An interviewer asks: "A restaurant partner changes how it reports preparation time and the values shift. No error is raised. How do you notice before customers complain, and how do you avoid an alarm that fires every hour?" Describe what you monitor and the trade-offs you tune.
