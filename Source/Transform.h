// Transform.h
#pragma once

#include "CoreMinimal.h"
#include "Transform.generated.h"

UCLASS()
class YOURPROJECT_API ATransform {
    GENERATED_BODY()

public:
    ATransform();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Transform")
    FVector Position;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Transform")
    FRotator Rotation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Transform")
    FVector Scale;

    UFUNCTION(BlueprintCallable, Category = "Transform")
    void Translate(FVector translation);
}
