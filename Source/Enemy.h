// Enemy.h
#pragma once

#include "CoreMinimal.h"
#include "Character.h"
#include "Enemy.generated.h"

UCLASS()
class YOURPROJECT_API AEnemy : public ACharacter {
    GENERATED_BODY()

public:
    AEnemy();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
    int Damage;

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void AttackPlayer(APlayerCharacter* player);

    UFUNCTION(BlueprintCallable, Category = "AI")
    void Patrol();

    UFUNCTION(BlueprintCallable, Category = "AI")
    void Flee();

    UFUNCTION(BlueprintCallable, Category = "Loot")
    void DropLoot();
}
