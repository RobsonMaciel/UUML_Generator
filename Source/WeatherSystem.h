// WeatherSystem.h
#pragma once

#include "CoreMinimal.h"
#include "WeatherSystem.generated.h"

UCLASS()
class YOURPROJECT_API AWeatherSystem {
    GENERATED_BODY()

public:
    AWeatherSystem();

    UFUNCTION(BlueprintCallable, Category = "Weather")
    void ChangeWeather(FString weatherType);

    UFUNCTION(BlueprintCallable, Category = "Weather")
    void SetWindSpeed(float speed);
}
