// Component.h
#pragma once

#include "CoreMinimal.h"
#include "Component.generated.h"

UCLASS()
class YOURPROJECT_API AComponent {
    GENERATED_BODY()

public:
    AComponent();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Component")
    FString Name;

    UFUNCTION(BlueprintCallable, Category = "Component")
    void Update();

    UFUNCTION(BlueprintCallable, Category = "Component")
    void Initialize();
}
