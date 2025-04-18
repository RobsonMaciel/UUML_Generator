// TimeManager.h
#pragma once

#include "CoreMinimal.h"
#include "TimeManager.generated.h"

UCLASS()
class YOURPROJECT_API ATimeManager {
    GENERATED_BODY()

public:
    ATimeManager();

    UFUNCTION(BlueprintCallable, Category = "Time")
    void SetTimeOfDay(float time);

    UFUNCTION(BlueprintCallable, Category = "Time")
    void PauseTime();

    UFUNCTION(BlueprintCallable, Category = "Time")
    void ResumeTime();
}
