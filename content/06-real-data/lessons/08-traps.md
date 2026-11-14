# Data traps


<p class="lede">Interviewers plant these on purpose. Calling one out earns points.</p>
<ul><li>Nulls in money columns, and denominators that still count them.</li><li>Cancelled orders with no delivery time.</li><li>Joins that duplicate rows: check the row count before and after.</li><li>Partial first or last week or month, which creates fake growth.</li><li>Division by zero for empty groups.</li><li>Ties in rankings: decide the rule and say it.</li><li>Dates stored as text and timezones.</li><li>Correlation vs causation: coupon users spend more, but coupons are targeted.</li><li>Tiny samples: a restaurant with 3 orders and a 100% late rate.</li></ul>
