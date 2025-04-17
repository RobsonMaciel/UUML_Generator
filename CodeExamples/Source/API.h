// API.h
#pragma once

#include "CoreMinimal.h"
#include "API.generated.h"

UCLASS()
class YOURPROJECT_API AAPI {
    GENERATED_BODY()

public:
    AAPI();

    UFUNCTION(BlueprintCallable, Category = "API")
    void Call(FString endpoint);

    UFUNCTION(BlueprintCallable, Category = "API")
    void Authenticate(FString token);
}
