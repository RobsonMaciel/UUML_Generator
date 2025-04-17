// Character.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Character.generated.h"

UCLASS()
class YOURPROJECT_API ACharacter : public ACharacter {
    GENERATED_BODY()

public:
    ACharacter();

protected:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Health;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Stamina;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Strength;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Agility;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Intelligence;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Level;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Experience;

public:
    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Move();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Jump();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Attack();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Defend();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Heal();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void UseItem();
}
