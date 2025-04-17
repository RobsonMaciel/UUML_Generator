// Environment.h
#pragma once

#include "CoreMinimal.h"
#include "Environment.generated.h"

UCLASS()
class YOURPROJECT_API AEnvironment {
    GENERATED_BODY()

public:
    AEnvironment();

    UFUNCTION(BlueprintCallable, Category = "Environment")
    FString GetOS();

    UFUNCTION(BlueprintCallable, Category = "Environment")
    FString GetUserName();
}
