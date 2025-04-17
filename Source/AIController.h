// AIController.h
#pragma once

#include "CoreMinimal.h"
#include "AIController.generated.h"

UCLASS()
class YOURPROJECT_API AAIController {
    GENERATED_BODY()

public:
    AAIController();

    UFUNCTION(BlueprintCallable, Category = "AI")
    void MoveToLocation(FVector location);

    UFUNCTION(BlueprintCallable, Category = "AI")
    void AttackTarget(class ACharacter* target);

    UFUNCTION(BlueprintCallable, Category = "AI")
    void FleeFromTarget(class ACharacter* target);

    UFUNCTION(BlueprintCallable, Category = "AI")
    void PatrolArea(FVector area);
}
