"""Stripe service for handling Stripe API operations."""

import stripe
from typing import Optional, Dict, Any

from pamfilico_python_stripe_sdk.models import (
    CustomerResponse,
    CustomerListResponse,
    CustomerData,
    CustomerListMeta,
    CustomerCreateInput,
    CustomerUpdateInput,
)


class StripeService:
    """Service class for Stripe operations.

    Handles Stripe API interactions with configurable API keys.
    Does not read from environment variables - keys must be provided explicitly.
    """

    def __init__(self, secret_key: str, publishable_key: str):
        """Initialize Stripe service with API keys.

        Args:
            secret_key: Stripe secret key (sk_test_... or sk_live_...)
            publishable_key: Stripe publishable key (pk_test_... or pk_live_...)

        Example:
            >>> service = StripeService(
            ...     secret_key="sk_test_...",
            ...     publishable_key="pk_test_..."
            ... )
        """
        self.secret_key = secret_key
        self.publishable_key = publishable_key

        # Set the Stripe API key for all operations
        stripe.api_key = self.secret_key

    def create_customer(
        self,
        data: CustomerCreateInput
    ) -> CustomerResponse:
        """Create a new Stripe customer.

        Args:
            data: CustomerCreateInput model with validated customer data

        Returns:
            CustomerResponse: Pydantic model containing:
                - data: CustomerData model with all customer fields
                - meta: Empty dictionary (for consistency)

        Example:
            >>> from pamfilico_python_stripe_sdk import CustomerCreateInput
            >>> input_data = CustomerCreateInput(
            ...     email="customer@example.com",
            ...     name="John Doe",
            ...     phone="+1234567890",
            ...     description="Premium customer",
            ...     metadata={"plan": "premium"}
            ... )
            >>> result = service.create_customer(input_data)
            >>> customer = result.data
            >>> print(customer.id)
            'cus_abc123...'
            >>> print(customer.email)
            'customer@example.com'
        """
        # Prepare Stripe customer data from validated input
        customer_data = {}
        if data.email:
            customer_data["email"] = data.email
        if data.name:
            customer_data["name"] = data.name
        if data.phone:
            customer_data["phone"] = data.phone
        if data.description:
            customer_data["description"] = data.description
        if data.metadata:
            customer_data["metadata"] = data.metadata

        # Create Stripe customer
        stripe_customer = stripe.Customer.create(**customer_data)

        # Serialize response
        customer_data = CustomerData(
            id=stripe_customer.id,
            email=stripe_customer.email,
            name=stripe_customer.name,
            phone=stripe_customer.phone,
            description=stripe_customer.description,
            balance=stripe_customer.balance,
            currency=stripe_customer.currency,
            delinquent=stripe_customer.delinquent,
            created=stripe_customer.created,
            metadata=dict(stripe_customer.metadata) if stripe_customer.metadata else {}
        )

        return CustomerResponse(data=customer_data, meta={})

    def get_customer(self, customer_id: str) -> CustomerResponse:
        """Get a single Stripe customer by ID.

        Args:
            customer_id: The Stripe customer ID (cus_...)

        Returns:
            CustomerResponse: Pydantic model containing:
                - data: CustomerData model with all customer fields
                - meta: Empty dictionary (for consistency)

        Example:
            >>> result = service.get_customer("cus_123abc")
            >>> customer = result.data
            >>> print(customer.email)
            'customer@example.com'
            >>> print(customer.name)
            'John Doe'
        """
        customer = stripe.Customer.retrieve(customer_id)

        customer_data = CustomerData(
            id=customer.id,
            email=customer.email,
            name=customer.name,
            phone=customer.phone,
            created=customer.created,
            balance=customer.balance,
            currency=customer.currency,
            delinquent=customer.delinquent,
            description=customer.description,
            metadata=dict(customer.metadata) if customer.metadata else {}
        )

        return CustomerResponse(data=customer_data, meta={})

    def update_customer(
        self,
        customer_id: str,
        data: CustomerUpdateInput
    ) -> CustomerResponse:
        """Update an existing Stripe customer.

        Args:
            customer_id: The Stripe customer ID (cus_...)
            data: CustomerUpdateInput model with validated update data

        Returns:
            CustomerResponse: Pydantic model containing:
                - data: CustomerData model with all updated customer fields
                - meta: Empty dictionary (for consistency)

        Example:
            >>> from pamfilico_python_stripe_sdk import CustomerUpdateInput
            >>> update_data = CustomerUpdateInput(
            ...     email="newemail@example.com",
            ...     name="Jane Doe",
            ...     metadata={"plan": "enterprise"}
            ... )
            >>> result = service.update_customer("cus_123abc", update_data)
            >>> customer = result.data
            >>> print(customer.email)
            'newemail@example.com'
        """
        # Prepare update data from validated input
        update_data = {}
        if data.email is not None:
            update_data["email"] = data.email
        if data.name is not None:
            update_data["name"] = data.name
        if data.phone is not None:
            update_data["phone"] = data.phone
        if data.description is not None:
            update_data["description"] = data.description
        if data.metadata is not None:
            update_data["metadata"] = data.metadata

        # Update Stripe customer
        stripe_customer = stripe.Customer.modify(customer_id, **update_data)

        # Serialize response
        customer_data = CustomerData(
            id=stripe_customer.id,
            email=stripe_customer.email,
            name=stripe_customer.name,
            phone=stripe_customer.phone,
            description=stripe_customer.description,
            balance=stripe_customer.balance,
            currency=stripe_customer.currency,
            delinquent=stripe_customer.delinquent,
            created=stripe_customer.created,
            metadata=dict(stripe_customer.metadata) if stripe_customer.metadata else {}
        )

        return CustomerResponse(data=customer_data, meta={})

    def get_customer_by_email(self, email: str) -> CustomerListResponse:
        """Get Stripe customers by email address.

        Note: Stripe allows multiple customers with the same email,
        so this returns a list of matching customers.

        Args:
            email: Customer email address (case-sensitive)

        Returns:
            CustomerListResponse: Pydantic model containing:
                - data: List of CustomerData models matching the email
                - meta: CustomerListMeta with pagination info (has_more, total_count, note)

        Example:
            >>> result = service.get_customer_by_email("customer@example.com")
            >>> print(result.meta.note)
            'Found 1 customer'
            >>> if result.data:
            ...     customer = result.data[0]  # Get first matching customer
            ...     print(customer.id)
            ...     'cus_abc123...'
        """
        # Fetch customers from Stripe filtered by email
        customers_response = stripe.Customer.list(email=email)

        # Serialize customer data
        customers_data = []
        for customer in customers_response.data:
            customers_data.append(CustomerData(
                id=customer.id,
                email=customer.email,
                name=customer.name,
                phone=customer.phone,
                created=customer.created,
                balance=customer.balance,
                currency=customer.currency,
                delinquent=customer.delinquent,
                description=customer.description,
                metadata=dict(customer.metadata) if customer.metadata else {}
            ))

        # Generate note message
        count = len(customers_data)
        note = f"Found {count} customer" if count == 1 else f"Found {count} customers"

        meta = CustomerListMeta(
            has_more=customers_response.has_more,
            total_count=count,
            note=note
        )

        return CustomerListResponse(data=customers_data, meta=meta)

    def list_customers(
        self,
        limit: int = 100,
        starting_after: Optional[str] = None
    ) -> CustomerListResponse:
        """List all Stripe customers with pagination.

        Args:
            limit: Number of customers to fetch per page (default: 100, max: 100)
            starting_after: Stripe customer ID to use as cursor for pagination

        Returns:
            CustomerListResponse: Pydantic model containing:
                - data: List of CustomerData models
                - meta: CustomerListMeta with pagination info (has_more, total_count)

        Example:
            >>> # List first page of customers
            >>> result = service.list_customers(limit=50)
            >>> customers = result.data
            >>> print(f"Found {result.meta.total_count} customers")
            Found 50 customers
            >>>
            >>> # Paginate to next page
            >>> if result.meta.has_more:
            ...     last_customer_id = customers[-1].id
            ...     next_page = service.list_customers(
            ...         limit=50,
            ...         starting_after=last_customer_id
            ...     )
            ...     next_customers = next_page.data
        """
        # Validate and cap limit
        limit = min(limit, 100)

        # Build Stripe API request parameters
        params = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after

        # Fetch customers from Stripe
        customers_response = stripe.Customer.list(**params)

        # Serialize customer data
        customers_data = []
        for customer in customers_response.data:
            customers_data.append(CustomerData(
                id=customer.id,
                email=customer.email,
                name=customer.name,
                created=customer.created,
                balance=customer.balance,
                currency=customer.currency,
                delinquent=customer.delinquent,
                description=customer.description,
                metadata=dict(customer.metadata) if customer.metadata else {}
            ))

        meta = CustomerListMeta(
            has_more=customers_response.has_more,
            total_count=len(customers_data)
        )

        return CustomerListResponse(data=customers_data, meta=meta)
