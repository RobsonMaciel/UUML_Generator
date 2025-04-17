// Application.h
#pragma once

#include "CoreMinimal.h"
#include "Application.generated.h"

UCLASS()
class YOURPROJECT_API AApplication {
    GENERATED_BODY()

public:
    AApplication();

    UFUNCTION(BlueprintCallable, Category = "Application")
    void Quit();

    UFUNCTION(BlueprintCallable, Category = "Application")
    void Minimize();
}
