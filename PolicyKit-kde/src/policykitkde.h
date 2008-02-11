#ifndef POLICYKITKDE_H
#define POLICYKITKDE_H

#define POLICYKITKDE_BUSNAME "org.freedesktop.PolicyKit.AuthenticationAgent"

struct PolicyService;

class PolicyKitKDE
{

public:
    PolicyKitKDE();
    ~PolicyKitKDE();

private:
    PolicyService *service;

};

#endif
