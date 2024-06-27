import pandas as pd
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.metrics import mean_squared_error
from django.http import Http404

from .serializers import ModelSerializer
from .models import ModelTarget

class ModelList(APIView):
    def get(self, request):
        reviews = ModelTarget.objects.all()
        serializer = ModelSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ModelSerializer(data=request.data)
        if serializer.is_valid():
            if 'csv_file' in request.FILES:
                csv_file = request.FILES['csv_file']
                original_filename = csv_file.name
                serializer.validated_data['csv_file'] = csv_file
                serializer.validated_data['original_filename'] = original_filename
                # CSV 파일을 처리하고 결과를 result에 저장
                df = pd.read_csv(csv_file)
                target = request.data.get('target')
                result = self.analyze_csv(df, target)
                serializer.validated_data['result'] = result
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def analyze_csv(self, df, target):
        # 데이터의 크기를 확인하고 샘플링
        if len(df) > 1000:
            df = df.sample(1000, random_state=42)

        df = df.dropna()

        # Transform columns with dtype='object' using Label_encoders
        label_encoders = {}
        for column in df.select_dtypes(include=['object']).columns:
            label_encoders[column] = LabelEncoder()
            df[column] = label_encoders[column].fit_transform(df[column].astype(str))

        linear_count = 0
        non_linear_count = 0

        # target 컬럼을 y로 설정
        y = df[target].values

        # 모든 열 조합에 대해 선형성 체크
        for col in df.columns:
            if col != target:
                x = df[col].values.reshape(-1, 1)

                # 선형 회귀 모델
                linear_regressor = LinearRegression()
                linear_regressor.fit(x, y)
                y_pred_linear = linear_regressor.predict(x)

                # 다항 회귀 모델 (2차)
                poly = PolynomialFeatures(degree=2)
                x_poly = poly.fit_transform(x)
                poly_regressor = LinearRegression()
                poly_regressor.fit(x_poly, y)
                y_pred_poly = poly_regressor.predict(x_poly)

                # 오차 계산
                mse_linear = mean_squared_error(y, y_pred_linear)
                mse_poly = mean_squared_error(y, y_pred_poly)

                # 다항 회귀 모델의 오차가 선형 회귀 모델의 오차보다 크게 작아지면 비선형으로 판단
                if mse_poly < mse_linear * 0.8:
                    non_linear_count += 1
                else:
                    linear_count += 1

        # 전체 결과를 종합하여 최종 선형성 판단
        if linear_count > non_linear_count:
            return 'linear'
        else:
            return 'non-linear'

class ModelDetail(APIView):
    def get_object(self, pk):
        try:
            return ModelTarget.objects.get(pk=pk)
        except ModelTarget.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        model = self.get_object(pk)
        serializer = ModelSerializer(model)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        model = self.get_object(pk)
        serializer = ModelSerializer(model, data=request.data)
        if serializer.is_valid():
            if 'csv_file' in request.FILES:
                csv_file = request.FILES['csv_file']
                original_filename = csv_file.name
                serializer.validated_data['csv_file'] = csv_file
                serializer.validated_data['original_filename'] = original_filename
                # CSV 파일을 처리하고 결과를 result에 저장
                df = pd.read_csv(csv_file)
                target = request.data.get('target')
                result = ModelList.analyze_csv(self, df, target)
                serializer.validated_data['result'] = result
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        model = self.get_object(pk)
        if model.csv_file:
            csv_file_path = os.path.join(settings.MEDIA_ROOT, model.csv_file.name)
            if os.path.exists(csv_file_path):
                os.remove(csv_file_path)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)