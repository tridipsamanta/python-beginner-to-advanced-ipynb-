import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
data = pd.DataFrame({
    'X1':[2,4,6,3,5],
    'X2':[3,5,7,8,10]
})

print("Original DataFrame ..")
print(data)

poly = PolynomialFeatures(degree=2,include_bias=False)
poly_feature = poly.fit_transform(data)
name = poly.get_feature_names_out(['X1','X2'])
final = pd.DataFrame(poly_feature,columns=name)
print(final)