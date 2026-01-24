import pandas as pd

from sklearn.preprocessing import PolynomialFeatures

data = pd.DataFrame({
    'X1':[2,4,5,3,5],
    'X2':[3,5,7,8,10]
})

print('Original Data : ')
print(data)

poly = PolynomialFeatures(degree=2,include_bias=False)
poly_features = poly.fit_transform(data)
features_name = poly.get_feature_names_out(['X1','X2'])
poly_df = pd.DataFrame(poly_features,columns=features_name)
print("Polynomial + interaction Features ......")
print(poly_df)