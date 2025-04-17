// Analytics.h
#pragma once

#include "CoreMinimal.h"
#include "Analytics.generated.h"

UCLASS()
class YOURPROJECT_API AAnalytics {
    GENERATED_BODY()

public:
    AAnalytics();

    UFUNCTION(BlueprintCallable, Category = "Analytics")
    void TrackEvent(FString eventName);

    UFUNCTION(BlueprintCallable, Category = "Analytics")
    void LogData(FString data);
}
